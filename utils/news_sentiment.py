import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "5e014dc18b224484ba053f4b9d7f2499")

def fetch_headlines(company_name, language='en', page_size=5):
    url = f"https://newsapi.org/v2/everything?q={company_name}&language={language}&pageSize={page_size}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"News API failed: {response.status_code} - {response.text}")

    data = response.json()
    return [article["title"] for article in data.get("articles", [])]

def get_sentiment_score(headlines):
    from transformers import pipeline
    sentiment_analyzer = pipeline("sentiment-analysis")
    sentiments = sentiment_analyzer(headlines)
    score = sum(1 if result["label"] == "POSITIVE" else -1 for result in sentiments)
    return round(score / len(sentiments), 2) if sentiments else 0.0
