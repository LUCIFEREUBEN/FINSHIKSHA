# FinLit AI - Financial Literacy Platform

AI-powered chatbot for financial education in multiple languages.

## Setup Instructions

### 1. Clone Repository
git clone LUCIFEREUBEN/FINSHIKSHA 
cd finlit-ai

text

### 2. Create Virtual Environment
python -m venv backend/venv

text

### 3. Activate Virtual Environment
**Windows:**
backend\venv\Scripts\activate

text

### 4. Install Dependencies
pip install -r requirements.txt

text

### 5. Add Training Data
Place your datasets in the `datasets/` folder.

### 6. Train Models (Optional)
python training/train_model.py

text

### 7. Run Backend
cd backend
python -m uvicorn app.main:app --reload

text

### 8. Run Frontend (New Terminal)
cd frontend
npm install
npm run dev

text

## Project Structure
- `backend/` - FastAPI backend server
- `frontend/` - Next.js frontend application
- `training/` - Model training scripts
- `datasets/` - Training data (not included)
- `models/` - Trained models (generate locally)

## Important Notes
- Virtual environment is NOT included in repository
- Models and datasets are NOT included (too large for Git)
- Train models locally after setup
- Requires Python 3.8+ and Node.js

Add this section after "4. Install Dependencies":​

text
### 4.5. Setup Environment Variables
Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key_here

text
Get your API key from https://console.groq.com
Save and commit:​

text
git add README.md
git commit -m "Update README with environment setup instructions"
git push origin main

## License
MIT License
