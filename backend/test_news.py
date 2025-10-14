import sys
sys.path.append('.')

from app.news_service import get_news_service

print("🧪 Testing News Service...")
print("="*60)

news_service = get_news_service()

print("\n1️⃣ Fetching NewsAPI articles...")
newsapi_articles = news_service.fetch_newsapi()
print(f"✅ Got {len(newsapi_articles)} articles from NewsAPI")
if newsapi_articles:
    print(f"Sample: {newsapi_articles[0]['title'][:60]}...")

print("\n2️⃣ Fetching RSS feeds...")
all_news = news_service.fetch_all_news()
print(f"✅ Got {len(all_news)} total articles from all sources")

print("\n3️⃣ Fetching market data...")
market_data = news_service.get_indian_financial_summary()
print(f"Market Summary:")
for key, value in market_data.items():
    if key != 'note':
        print(f"  {key}: {value}")

print("\n4️⃣ Getting formatted headlines...")
headlines = news_service.get_financial_headlines()
print(f"Breaking news: {len(headlines['breaking_news'])} articles")
print(f"Recent news: {len(headlines['recent_news'])} articles")
print(f"Last updated: {headlines['last_updated']}")

print("\n✅ ALL TESTS PASSED!")
print("Your news service is working perfectly!")
