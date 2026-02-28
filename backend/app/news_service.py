"""
Real-time Financial News Service
Fetches news from multiple sources: NewsAPI, RSS feeds, official sources
"""
import requests
from datetime import datetime, timedelta
import feedparser
from typing import List, Dict
import json
from pathlib import Path

class FinancialNewsService:
    def __init__(self):
        # NewsAPI.org - Get FREE API key at https://newsapi.org/
        # Sign up and get your key (100 requests/day FREE)
        self.newsapi_key = ""  # Replace with your key
        
        # RSS Feeds (No API key needed - always FREE)
        self.rss_feeds = {
            "rbi": "https://www.rbi.org.in/Scripts/RSS/RBIMasterCirculars.xml",
            "sebi": "https://www.sebi.gov.in/rss/all.rss",
            "economic_times": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
            "moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
            "business_standard": "https://www.business-standard.com/rss/latest.rss"
        }
        
        self.cache_file = Path("out/news_cache.json")
        self.cache_duration = 1800  # 30 minutes cache
    
def get_cached_news(self):
    if self.cache_file.exists():
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)  # <-- can raise JSONDecodeError
            cache_time = datetime.fromisoformat(cache['timestamp'])  # <-- KeyError/ValueError
            if datetime.now() - cache_time < timedelta(seconds=self.cache_duration):
                return cache['news']
    return None

    
    def save_cache(self, news):
        """Save news to cache"""
        cache = {
            'timestamp': datetime.now().isoformat(),
            'news': news
        }
        self.cache_file.parent.mkdir(exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    
    def fetch_newsapi(self) -> List[Dict]:
        """Fetch from NewsAPI.org"""
        if self.newsapi_key == "YOUR_NEWSAPI_KEY_HERE":
            return []  # Skip if no key configured
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": self.newsapi_key,
                "country": "in",
                "category": "business",
                "pageSize": 10
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('articles', [])[:10]:
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'NewsAPI'),
                        'published_at': article.get('publishedAt', ''),
                        'category': 'business'
                    })
                return articles
        except Exception as e:
            print(f"NewsAPI error: {e}")
        
        return []
    
    def fetch_rss_feed(self, feed_name: str, feed_url: str) -> List[Dict]:
        """Fetch from RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:5]:  # Get 5 items per feed
                # Parse published date
                published = entry.get('published', '')
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6]).isoformat()
                
                articles.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', '')[:200],  # Limit description
                    'url': entry.get('link', ''),
                    'source': feed_name.upper(),
                    'published_at': published,
                    'category': 'financial_news'
                })
            
            return articles
        except Exception as e:
            print(f"RSS feed {feed_name} error: {e}")
        
        return []
    
    def fetch_all_news(self) -> List[Dict]:
        """Fetch news from all sources"""
        # Check cache first
        cached = self.get_cached_news()
        if cached:
            return cached
        
        all_news = []
        
        # Fetch from NewsAPI (if configured)
        newsapi_articles = self.fetch_newsapi()
        all_news.extend(newsapi_articles)
        
        # Fetch from RSS feeds
        for feed_name, feed_url in self.rss_feeds.items():
            feed_articles = self.fetch_rss_feed(feed_name, feed_url)
            all_news.extend(feed_articles)
        
        # Sort by published date (newest first)
        all_news.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        
        # Limit to top 20 news items
        all_news = all_news[:20]
        
        # Save to cache
        self.save_cache(all_news)
        
        return all_news
    
    def get_indian_financial_summary(self) -> Dict:
        """Get a summary of Indian financial markets"""
        try:
            # This uses Alpha Vantage FREE API (no key needed for basic data)
            # Or fallback to Yahoo Finance
            
            summary = {
                "sensex": "Market data unavailable in free tier",
                "nifty": "Market data unavailable in free tier",
                "usd_inr": "Check live rates",
                "gold": "Check live rates",
                "crude_oil": "Check live rates",
                "note": "Install yfinance for live market data: pip install yfinance"
            }
            
            # Try to get basic data without API key
            try:
                import yfinance as yf
                
                # Get Indian market indices
                sensex = yf.Ticker("^BSESN")
                nifty = yf.Ticker("^NSEI")
                
                sensex_data = sensex.history(period="1d")
                nifty_data = nifty.history(period="1d")
                
                if not sensex_data.empty:
                    summary["sensex"] = f"₹{sensex_data['Close'].iloc[-1]:.2f}"
                
                if not nifty_data.empty:
                    summary["nifty"] = f"₹{nifty_data['Close'].iloc[-1]:.2f}"
            
            except ImportError:
                pass  # yfinance not installed
            except Exception as e:
                print(f"Market data error: {e}")
            
            return summary
        
        except Exception as e:
            print(f"Summary error: {e}")
            return {}
    
    def get_financial_headlines(self, lang="en") -> Dict:
        """Get formatted financial headlines for frontend"""
        news = self.fetch_all_news()
        market_summary = self.get_indian_financial_summary()
        
        # Categorize news
        breaking = news[:3]  # Top 3 as breaking
        recent = news[3:10]  # Next 7 as recent
        
        return {
            "breaking_news": breaking,
            "recent_news": recent,
            "market_summary": market_summary,
            "last_updated": datetime.now().isoformat(),
            "total_articles": len(news)
        }


# Global instance
news_service = None

def get_news_service():
    """Get or create news service instance"""
    global news_service
    if news_service is None:
        news_service = FinancialNewsService()
    return news_service
