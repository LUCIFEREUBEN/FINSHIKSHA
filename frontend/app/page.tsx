'use client';

import { useState, useEffect, useRef } from 'react';
import { 
  Mic, Send, DollarSign, AlertCircle, 
  Sparkles, BookOpen, BarChart3, Loader2, 
  CheckCircle, XCircle, Shield, Award, 
  Play, TrendingUp, CreditCard, Zap, 
  Newspaper, RefreshCw, Square, MicOff
} from 'lucide-react';

// ===== NEWS TICKER =====
function NewsTicker() {
  const [news, setNews] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetchNews();
    const interval = setInterval(fetchNews, 1800000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (news?.breaking_news?.length > 0) {
      const interval = setInterval(() => {
        setCurrentIndex((prev) => (prev + 1) % news.breaking_news.length);
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [news]);

  const fetchNews = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/news?lang=en');
      const data = await res.json();
      setNews(data);
      setLoading(false);
      setError('');
    } catch (error) {
      setError('Failed to load news');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-r from-red-50 to-orange-50 border-b border-red-200 px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center gap-3">
          <Loader2 className="w-4 h-4 text-red-600 animate-spin" />
          <p className="text-sm text-red-700">Loading financial news...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gradient-to-r from-red-50 to-orange-50 border-b border-red-200 px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center gap-3">
          <XCircle className="w-4 h-4 text-red-600" />
          <p className="text-sm text-red-700">{error}</p>
          <button onClick={fetchNews} className="ml-auto text-xs text-red-600 hover:text-red-800">Retry</button>
        </div>
      </div>
    );
  }

  if (!news?.breaking_news?.length) {
    return (
      <div className="bg-gradient-to-r from-blue-50 to-cyan-50 border-b border-blue-200 px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center gap-3">
          <Newspaper className="w-4 h-4 text-blue-600" />
          <p className="text-sm text-blue-700">📰 No breaking news</p>
        </div>
      </div>
    );
  }

  const currentNews = news.breaking_news[currentIndex];

  return (
    <div className="bg-gradient-to-r from-red-50 via-orange-50 to-yellow-50 border-b border-red-200">
      <div className="max-w-6xl mx-auto px-4 py-3">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0">
            <div className="bg-gradient-to-r from-red-600 to-orange-600 px-3 py-1 rounded-lg flex items-center gap-2 shadow-lg">
              <Newspaper className="w-3 h-3 text-white" />
              <span className="text-xs font-bold text-white uppercase tracking-wide">Breaking</span>
            </div>
          </div>
          <div className="flex-1 min-w-0">
            <a href={currentNews.url} target="_blank" rel="noopener noreferrer" className="block hover:text-red-700 transition">
              <p className="text-sm font-semibold text-gray-900 truncate">{currentNews.title}</p>
              <p className="text-xs text-gray-600 truncate">
                {currentNews.source} • {new Date(currentNews.published_at).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
              </p>
            </a>
          </div>
          <div className="flex-shrink-0 flex items-center gap-2">
            {news.breaking_news.map((_: any, idx: number) => (
              <button key={idx} onClick={() => setCurrentIndex(idx)} className={`w-2 h-2 rounded-full transition ${idx === currentIndex ? 'bg-red-600' : 'bg-gray-300'}`} />
            ))}
            <button onClick={fetchNews} className="ml-2 p-1 hover:bg-red-100 rounded transition" title="Refresh">
              <RefreshCw className="w-3 h-3 text-red-600" />
            </button>
          </div>
        </div>
      </div>
      {news.market_summary && (
        <div className="border-t border-red-200 bg-white/50">
          <div className="max-w-6xl mx-auto px-4 py-2">
            <div className="grid grid-cols-5 gap-3">
              {Object.entries(news.market_summary).filter(([key]) => !['note'].includes(key)).map(([key, value]: [string, any]) => (
                <div key={key} className="text-center">
                  <p className="text-xs text-gray-500 uppercase tracking-wide">{key.replace('_', ' ')}</p>
                  <p className="text-sm font-bold text-gray-900">{value}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ===== MAIN COMPONENT =====
export default function FinLitAI() {
  const [question, setQuestion] = useState('');
  const [language, setLanguage] = useState('en');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [profile, setProfile] = useState({ income: '', expenses: '', emi: '' });
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const recognitionRef = useRef<any>(null);

  const languageLabels: any = {
    en: 'English',
    hi: 'हिंदी',
    kn: 'ಕನ್ನಡ'
  };

  const content: any = {
    en: {
      badge: "SEBI/RBI Compliant Platform",
      title: "Your Financial Literacy Companion",
      subtitle: "AI-powered guidance for smarter money decisions",
      features: [
        { icon: Shield, text: "Bank-level Security" },
        { icon: Zap, text: "Instant AI Analysis" },
        { icon: Award, text: "Personalized Advice" },
        { icon: BarChart3, text: "Real-time Insights" }
      ],
      popularLabel: "Popular Questions",
      questions: [
        "What is an asset?",
        "Explain EMI simply",
        "How much should I save?",
        "What is investment?",
        "Tell me about emergency fund",
        "What are mutual funds?"
      ],
      toggleLabel: "Enable Smart Financial Analysis",
      placeholder: "Ask anything about money, savings, investments...",
      button: "Get AI Answer",
      disclaimer: "Educational Purpose Only",
      disclaimerText: "This is not investment advice. Consult SEBI-registered financial advisors for personalized recommendations.",
      footer: "Built with ❤️ for Financial Literacy in India",
      compliance: "Compliant with SEBI & RBI Guidelines"
    },
    hi: {
      badge: "SEBI/RBI अनुपालन प्लेटफ़ॉर्म",
      title: "आपका वित्तीय साक्षरता साथी",
      subtitle: "बेहतर पैसे के फैसलों के लिए AI-संचालित मार्गदर्शन",
      features: [
        { icon: Shield, text: "Bank-level Security" },
        { icon: Zap, text: "Instant AI Analysis" },
        { icon: Award, text: "Personalized Advice" },
        { icon: BarChart3, text: "Real-time Insights" }
      ],
      popularLabel: "लोकप्रिय प्रश्न",
      questions: [
        "संपत्ति क्या है?",
        "EMI क्या होता है?",
        "कितनी बचत करूं?",
        "निवेश क्या है?",
        "Emergency fund बताएं"
      ],
      toggleLabel: "स्मार्ट वित्तीय विश्लेषण सक्षम करें",
      placeholder: "पैसे, बचत, निवेश के बारे में कुछ भी पूछें...",
      button: "AI उत्तर पाएं",
      disclaimer: "केवल शैक्षिक उद्देश्य",
      disclaimerText: "यह निवेश सलाह नहीं है। SEBI-पंजीकृत सलाहकारों से परामर्श करें।",
      footer: "Built with ❤️ for Financial Literacy in India",
      compliance: "SEBI और RBI दिशानिर्देशों के अनुरूप"
    },
    kn: {
      badge: "SEBI/RBI ಅನುಸರಣೆ ವೇದಿಕೆ",
      title: "ನಿಮ್ಮ ಹಣಕಾಸು ಸಾಕ್ಷರತೆ ಸಂಗಾತಿ",
      subtitle: "ಉತ್ತಮ ಹಣ ನಿರ್ಧಾರಗಳಿಗಾಗಿ AI-ಚಾಲಿತ ಮಾರ್ಗದರ್ಶನ",
      features: [
        { icon: Shield, text: "Bank-level Security" },
        { icon: Zap, text: "Instant AI Analysis" },
        { icon: Award, text: "Personalized Advice" },
        { icon: BarChart3, text: "Real-time Insights" }
      ],
      popularLabel: "ಜನಪ್ರಿಯ ಪ್ರಶ್ನೆಗಳು",
      questions: [
        "ಆಸ್ತಿ ಎಂದರೇನು?",
        "EMI ಅರ್ಥವೇನು?",
        "ಎಷ್ಟು ಉಳಿಸಬೇಕು?",
        "ಹೂಡಿಕೆ ಎಂದರೇನು?"
      ],
      toggleLabel: "ಸ್ಮಾರ್ಟ್ ಹಣಕಾಸು ವಿಶ್ಲೇಷಣೆ ಸಕ್ರಿಯಗೊಳಿಸಿ",
      placeholder: "ಹಣ, ಉಳಿತಾಯ, ಹೂಡಿಕೆ ಬಗ್ಗೆ ಏನು ಬೇಕಾದರೂ ಕೇಳಿ...",
      button: "AI ಉತ್ತರ ಪಡೆಯಿರಿ",
      disclaimer: "ಶೈಕ್ಷಣಿಕ ಉದ್ದೇಶಕ್ಕಾಗಿ ಮಾತ್ರ",
      disclaimerText: "ಇದು ಹೂಡಿಕೆ ಸಲಹೆ ಅಲ್ಲ। SEBI-ನೋಂದಾಯಿತ ಸಲಹೆಗಾರರನ್ನು ಸಂಪರ್ಕಿಸಿ।",
      footer: "Built with ❤️ for Financial Literacy in India",
      compliance: "SEBI ಮತ್ತು RBI ಮಾರ್ಗಸೂಚಿಗಳ ಅನುಸಾರ"
    }
  };

  const currentContent = content[language];

  // ===== VOICE INPUT =====
  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('❌ Voice input only works in Chrome/Edge browser.');
      return;
    }

    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    try {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      const recognition = new SpeechRecognition();
      
      const langCode = language === 'hi' ? 'hi-IN' : language === 'kn' ? 'kn-IN' : 'en-IN';
      recognition.lang = langCode;
      recognition.continuous = false;
      recognition.interimResults = true;

      recognition.onstart = () => {
        setIsListening(true);
        setError('');
        console.log('🎤 LISTENING:', langCode);
      };
      
      recognition.onend = () => {
        setIsListening(false);
        recognitionRef.current = null;
        console.log('🎤 STOPPED');
      };
      
      recognition.onresult = (event: any) => {
        const transcript = Array.from(event.results).map((result: any) => result[0].transcript).join('');
        console.log('📝 YOU SAID:', transcript);
        setQuestion(transcript);
      };

      recognition.onerror = (event: any) => {
        console.error('❌ ERROR:', event.error);
        setIsListening(false);
        recognitionRef.current = null;
        
        if (event.error === 'not-allowed') {
          alert('🎤 Microphone blocked! Click lock icon in address bar → Allow microphone → Refresh page');
        } else if (event.error === 'no-speech') {
          setError('No speech detected. Try again.');
        } else if (event.error === 'audio-capture') {
          alert('❌ No microphone found.');
        } else {
          setError(`Voice error: ${event.error}`);
        }
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (err: any) {
      console.error('❌ FAILED:', err);
      alert('Voice input failed. Use Chrome browser.');
      setIsListening(false);
    }
  };

  // ===== SUBMIT QUESTION =====
  const handleSubmit = async () => {
    if (!question.trim() && !showProfile) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const payload: any = { question: question || "Analyze my financial health", language };
      
      if (showProfile && profile.income && profile.expenses) {
        payload.user_profile = {
          income: parseFloat(profile.income),
          expenses: parseFloat(profile.expenses),
          emi: parseFloat(profile.emi || '0')
        };
      }

      const res = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Backend error');
      setResponse(await res.json());
    } catch (error) {
      setError('Backend not running. Start: uvicorn app.main:app --reload');
    } finally {
      setLoading(false);
    }
  };

  // ===== TEXT-TO-SPEECH (Browser) =====
  const readAloud = (text: string) => {
    if (!('speechSynthesis' in window)) {
      alert('❌ Text-to-speech not supported');
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      utteranceRef.current = null;
      return;
    }

    const speak = () => {
      window.speechSynthesis.cancel();
      
      const utterance = new SpeechSynthesisUtterance(text);
      const voices = window.speechSynthesis.getVoices();
      
      const langCode = language === 'hi' ? 'hi-IN' : language === 'kn' ? 'kn-IN' : 'en-IN';
      
      let voice = voices.find(v => v.lang === langCode) ||
                  voices.find(v => v.lang.startsWith(langCode.split('-')[0])) ||
                  voices.find(v => v.lang.includes('IN')) ||
                  voices.find(v => v.lang.startsWith('en')) ||
                  voices[0];
      
      if (voice) {
        utterance.voice = voice;
        console.log('✅ VOICE:', voice.name, voice.lang);
      }
      
      utterance.lang = langCode;
      utterance.rate = 0.85;
      utterance.pitch = 1;
      utterance.volume = 1;
      
      utterance.onstart = () => {
        setIsSpeaking(true);
        console.log('🔊 SPEAKING');
      };
      
      utterance.onend = () => {
        setIsSpeaking(false);
        utteranceRef.current = null;
        console.log('🔊 FINISHED');
      };
      
      utterance.onerror = (e) => {
        if (e.error === 'interrupted' || e.error === 'canceled') {
          setIsSpeaking(false);
          return;
        }
        console.error('❌ SPEECH ERROR:', e.error);
        setIsSpeaking(false);
      };

      utteranceRef.current = utterance;
      window.speechSynthesis.speak(utterance);
    };

    const voices = window.speechSynthesis.getVoices();
    if (voices.length === 0) {
      window.speechSynthesis.onvoiceschanged = speak;
      setTimeout(speak, 300);
    } else {
      speak();
    }
  };

  // ===== TEXT-TO-SPEECH (Google) =====
  const readAloudGoogle = async (text: string) => {
    try {
      if (isSpeaking) {
        setIsSpeaking(false);
        return;
      }

      const langCode = language === 'hi' ? 'hi' : language === 'kn' ? 'kn' : 'en';
      const url = `https://translate.google.com/translate_tts?ie=UTF-8&tl=${langCode}&client=tw-ob&q=${encodeURIComponent(text)}`;
      
      const audio = new Audio(url);
      
      audio.onplay = () => {
        setIsSpeaking(true);
        console.log('🔊 Google TTS:', langCode);
      };
      
      audio.onended = () => {
        setIsSpeaking(false);
        console.log('🔊 Finished');
      };
      
      audio.onerror = () => {
        setIsSpeaking(false);
        console.error('❌ Google TTS failed');
        setError('Audio playback failed');
      };
      
      await audio.play();
    } catch (err) {
      console.error('❌ Error:', err);
      setError('Failed to play audio');
      setIsSpeaking(false);
    }
  };

  // ===== CLEANUP =====
  useEffect(() => {
    return () => {
      if (window.speechSynthesis) window.speechSynthesis.cancel();
      if (recognitionRef.current) recognitionRef.current.stop();
    };
  }, []);

  const metricsData = response?.metrics ? [
    { label: 'Monthly Savings', value: `₹${response.metrics.savings.toLocaleString()}`, icon: TrendingUp, bg: 'from-emerald-50 to-teal-50', shadow: 'from-emerald-500 to-teal-600' },
    { label: 'Savings Rate', value: `${response.metrics.savings_rate}%`, icon: BarChart3, bg: 'from-blue-50 to-cyan-50', shadow: 'from-blue-500 to-cyan-600' },
    { label: 'EMI Share', value: `${response.metrics.emi_share}%`, icon: CreditCard, bg: 'from-orange-50 to-amber-50', shadow: 'from-orange-500 to-amber-600' },
    { label: 'Expense Ratio', value: `${response.metrics.expense_ratio}%`, icon: DollarSign, bg: 'from-violet-50 to-purple-50', shadow: 'from-violet-500 to-purple-600' }
  ] : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-50/30 relative">
      <div className="fixed inset-0 pointer-events-none z-0">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="dotPattern" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
              <circle cx="2" cy="2" r="1.5" fill="rgba(0, 0, 0, 0.08)" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#dotPattern)" />
        </svg>
      </div>

      <div className="relative z-10">
        <NewsTicker />
      </div>

      <header className="relative sticky top-0 z-50 bg-white/90 backdrop-blur-lg border-b border-gray-200/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-teal-400 to-blue-500 rounded-xl blur opacity-50"></div>
                <div className="relative bg-gradient-to-br from-teal-500 to-blue-600 p-2.5 rounded-xl">
                  <DollarSign className="w-6 h-6 text-white" strokeWidth={2.5} />
                </div>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">FinShiksha</h1>
                <p className="text-xs text-gray-500 flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  Powered by Transformer AI
                </p>
              </div>
            </div>
            
            <div className="flex gap-2">
              {['en', 'hi', 'kn'].map((lang) => (
                <button
                  key={lang}
                  onClick={() => setLanguage(lang)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    language === lang ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {languageLabels[lang]}
                </button>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-teal-50 border border-teal-200 rounded-full text-xs font-medium text-teal-700 mb-6">
            <Shield className="w-3.5 h-3.5" />
            {currentContent.badge}
          </div>
          
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">{currentContent.title}</h2>
          <p className="text-lg text-gray-600 mb-8">{currentContent.subtitle}</p>

          <div className="flex flex-wrap justify-center gap-3">
            {currentContent.features.map((f: any, i: number) => (
              <div key={i} className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-full text-sm">
                <f.icon className="w-4 h-4 text-gray-600" />
                <span className="text-gray-700 font-medium">{f.text}</span>
              </div>
            ))}
          </div>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3">
            <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        <div className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-gray-600" />
            <p className="text-sm font-semibold text-gray-700">{currentContent.popularLabel}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {currentContent.questions.map((q: string, i: number) => (
              <button
                key={i}
                onClick={() => setQuestion(q)}
                className="px-4 py-2 bg-white hover:bg-gray-50 border border-gray-200 hover:border-gray-300 rounded-lg text-sm text-gray-700 transition"
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-8">
          <label className="flex items-center gap-3 mb-6 cursor-pointer w-fit">
            <div className="relative">
              <input
                type="checkbox"
                checked={showProfile}
                onChange={(e) => setShowProfile(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 rounded-full peer-checked:bg-teal-500 transition"></div>
              <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition peer-checked:translate-x-5"></div>
            </div>
            <BarChart3 className="w-5 h-5 text-gray-600" />
            <span className="text-sm font-medium text-gray-700">{currentContent.toggleLabel}</span>
          </label>

          {showProfile && (
            <div className="grid grid-cols-3 gap-4 mb-6 p-4 bg-gray-50 rounded-xl">
              <input type="number" placeholder="Income ₹" value={profile.income} onChange={(e) => setProfile({...profile, income: e.target.value})} className="px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:border-teal-500" />
              <input type="number" placeholder="Expenses ₹" value={profile.expenses} onChange={(e) => setProfile({...profile, expenses: e.target.value})} className="px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:border-teal-500" />
              <input type="number" placeholder="EMI ₹" value={profile.emi} onChange={(e) => setProfile({...profile, emi: e.target.value})} className="px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:border-teal-500" />
            </div>
          )}

          <div className="flex gap-3">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
              placeholder={currentContent.placeholder}
              className="flex-1 px-5 py-4 bg-gray-50 border border-gray-300 rounded-xl text-gray-900 focus:outline-none focus:border-teal-500"
            />
            <button 
              onClick={handleVoiceInput} 
              className={`p-4 border rounded-xl transition ${
                isListening ? 'bg-red-100 border-red-300 animate-pulse' : 'bg-gray-100 hover:bg-gray-200 border-gray-300'
              }`}
              title={isListening ? 'Stop' : 'Voice input'}
            >
              {isListening ? <MicOff className="w-5 h-5 text-red-600" /> : <Mic className="w-5 h-5 text-gray-700" />}
            </button>
            <button onClick={handleSubmit} disabled={loading} className="px-6 py-4 bg-teal-500 hover:bg-teal-600 text-white rounded-xl font-medium transition disabled:opacity-50 flex items-center gap-2">
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {response && (
          <div className="space-y-6">
            {response.metrics && metricsData.length > 0 && (
              <div className="grid grid-cols-4 gap-4">
                {metricsData.map((m, i) => (
                  <div key={i} className="relative group">
                    <div className={`absolute inset-0 bg-gradient-to-br ${m.shadow} rounded-xl blur opacity-20 group-hover:opacity-30 transition`}></div>
                    <div className={`relative bg-gradient-to-br ${m.bg} border border-gray-200 rounded-xl p-5`}>
                      <m.icon className="w-5 h-5 text-gray-700 mb-2" />
                      <p className="text-xs font-semibold text-gray-600 mb-1">{m.label}</p>
                      <p className="text-2xl font-bold text-gray-900">{m.value}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="bg-white rounded-2xl border border-gray-200 p-6">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-teal-500" />
                  Your AI Answer
                </h3>
                <button 
                  onClick={() => {
                    if (language === 'kn') {
                      readAloudGoogle(response.text);
                    } else {
                      readAloud(response.text);
                    }
                  }}
                  className={`px-3 py-2 rounded-lg text-sm flex items-center gap-2 transition font-medium ${
                    isSpeaking ? 'bg-red-100 hover:bg-red-200 text-red-700' : 'bg-teal-50 hover:bg-teal-100 text-teal-700'
                  }`}
                >
                  {isSpeaking ? (
                    <>
                      <Square className="w-4 h-4" />
                      Stop
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4" />
                      Read
                    </>
                  )}
                </button>
              </div>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">{response.text}</p>
            </div>
          </div>
        )}

        <div className="mt-8 bg-amber-50 border border-amber-200 rounded-xl p-5 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-bold text-amber-900 mb-1">{currentContent.disclaimer}</p>
            <p className="text-sm text-amber-800">{currentContent.disclaimerText}</p>
          </div>
        </div>
      </main>

      <footer className="relative z-10 bg-white border-t border-gray-200 py-6 mt-12">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p className="text-sm text-gray-600">{currentContent.footer}</p>
          <p className="text-xs text-gray-500 mt-1 flex items-center justify-center gap-1.5">
            <Shield className="w-3 h-3" />
            {currentContent.compliance}
          </p>
        </div>
      </footer>
    </div>
  );
}
