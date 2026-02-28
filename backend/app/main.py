from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict
from pathlib import Path
from dotenv import load_dotenv
from gtts import gTTS
from groq import Groq
import requests
import os
from datetime import datetime

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys - Set these as environment variables (e.g., in Vercel dashboard or .env file)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Pydantic models
class UserProfile(BaseModel):
    income: float
    expenses: float
    emi: float = 0.0

class QuestionRequest(BaseModel):
    question: str
    language: str = "en"
    user_profile: Optional[UserProfile] = None

# Language mapping for gTTS
LANG_MAP = {
    "en": "en",
    "hi": "hi",
    "kn": "kn"
}

# Language names for prompts
LANG_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada"
}

@app.post("/ask")


async def ask_question(request: QuestionRequest):
    try:
        question = request.question
        language = request.language
        profile = request.user_profile
        
        # Calculate financial metrics if profile provided
        metrics = None
        profile_context = ""
        
        if profile:
            savings = profile.income - profile.expenses - profile.emi
            savings_rate = round((savings / profile.income * 100), 1) if profile.income > 0 else 0
            emi_share = round((profile.emi / profile.income * 100), 1) if profile.income > 0 else 0
            expense_ratio = round((profile.expenses / profile.income * 100), 1) if profile.income > 0 else 0
            
            metrics = {
                "savings": int(savings),
                "savings_rate": savings_rate,
                "emi_share": emi_share,
                "expense_ratio": expense_ratio
            }
            
            profile_context = f"""
User's Financial Profile:
- Monthly Income: ₹{profile.income:,.0f}
- Monthly Expenses: ₹{profile.expenses:,.0f}
- Monthly EMI: ₹{profile.emi:,.0f}
- Monthly Savings: ₹{savings:,.0f}
- Savings Rate: {savings_rate}%
"""
        
        # Create prompt
        prompt = f"""You are a financial literacy assistant for Indian users. Answer in {LANG_NAMES.get(language, 'English')}.

{profile_context}

Question: {question}

Rules:
1. Answer in {LANG_NAMES.get(language, 'English')} language ONLY
2. Keep answers simple and practical (under 150 words)
3. Use Indian financial terms (₹, SIP, mutual funds, FD, PPF, etc.)
4. If profile is provided, give personalized advice
5. Use 1-2 emojis maximum
6. Format: Main advice + 2-3 bullet points if needed

Answer:"""

        # Get response from Groq
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Generate audio with correct language
        lang_code = LANG_MAP.get(language, "en")
        audio_path = Path("audio/speech.mp3")
        audio_path.parent.mkdir(exist_ok=True)
        
        try:
            tts = gTTS(text=response_text, lang=lang_code, slow=False)
            tts.save(str(audio_path))
            audio_generated = True
        except Exception as audio_error:
            print(f"Audio generation failed: {audio_error}")
            audio_generated = False
        
        # Prepare response
        result = {
            "text": response_text,
            "language": language,
            "audio": audio_generated,
            "sources": [
                {"topic": "Financial Literacy", "confidence": 0.95},
                {"topic": "Personal Finance", "confidence": 0.90}
            ]
        }
        
        if metrics:
            result["metrics"] = metrics
        
        return result
        
    except Exception as e:
        print(f"Error in ask_question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/speech.mp3")
async def get_audio():
    audio_path = Path("audio/speech.mp3")
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path, media_type="audio/mpeg")

@app.get("/news")
async def get_news(lang: str):
    try:
        url = f"https://newsapi.org/v2/top-headlines"
        params = {
            "country": "in",
            "category": "business",
            "apiKey": NEWS_API_KEY,
            "pageSize": 10
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("status") != "ok":
            raise HTTPException(status_code=500, detail="Failed to fetch news")
        
        articles = data.get("articles", [])[:5]
        breaking_news = []
        
        for article in articles:
            breaking_news.append({
                "title": article.get("title", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", "")
            })
        
        market_summary = {
            "sensex": "81,455 ▲ 0.8%",
            "nifty": "24,857 ▲ 0.6%",
            "gold": "₹73,450/10g ▼ 0.3%",
            "crude_oil": "$74.25 ▲ 1.2%",
            "usd_inr": "₹83.15 ▲ 0.1%"
        }
        
        return {
            "breaking_news": breaking_news,
            "market_summary": market_summary,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "FinShiksha API",
        "version": "1.0.0",
        "status": "running",
        "ai_model": "Groq Llama 3.3 70B"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
