import os
import sys
import json
import time
import textwrap
import requests
import tweepy
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Credentials are loaded from Environment Variables for security
NEWSDATA_API_KEY = os.environ.get("NEWSDATA_API_KEY")
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")

HISTORY_FILE = "posted_history.json"
MAX_CHARACTERS = 280

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_history(history_list):
    # Keep only the last 500 IDs to avoid indefinite growth
    history_list = history_list[-500:] 
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_list, f, indent=2)

def fetch_news():
    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": NEWSDATA_API_KEY,
        "country": "in",
        "language": "en",
        "category": "top"
        # Removed duplication=1 as it's a paid feature or sometimes unreliable, handled locally
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "success":
            print(f"Error fetching news: {data}")
            return []
        
        return data.get("results", [])
    except Exception as e:
        print(f"Exception during news fetch: {e}")
        return []

def download_image(image_url):
    if not image_url:
        return None
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            filename = "temp_image.jpg"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

def process_and_post():
    if not all([NEWSDATA_API_KEY, X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]):
        print("Missing API Secrets. Please set them in Environment Variables.")
        sys.exit(1)

    # authentication for v2 (Tweeting)
    client_v2 = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET
    )

    history = load_history()
    articles = fetch_news()
    
    print(f"Fetched {len(articles)} articles.")

    # Get top 3 unique news articles not already posted
    top_news = []
    for article in articles:
        article_id = article.get("article_id") or article.get("link")
        
        if article_id in history:
            continue
        
        title = article.get("title", "").strip()
        if title and len(top_news) < 3:
            top_news.append({"id": article_id, "title": title})
    
    if not top_news:
        print("No new unique news to post.")
        return
    
    # Build single tweet with top 3 headlines
    tweet_lines = ["📰 Top Breaking News:\n"]
    for i, news in enumerate(top_news, 1):
        # Truncate title if needed (max ~80 chars each to fit in 280)
        title = news["title"]
        if len(title) > 80:
            title = title[:77] + "..."
        tweet_lines.append(f"{i}. {title}")
    
    tweet_text = "\n".join(tweet_lines)
    
    # Ensure we stay under 280 characters
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
    
    print(f"Posting combined news tweet ({len(tweet_text)} chars)...")
    print(tweet_text)
    
    try:
        response = client_v2.create_tweet(text=tweet_text)
        tweet_id = response.data['id']
        print(f"✅ Posted successfully: https://x.com/i/status/{tweet_id}")
        
        # Mark all included articles as posted
        for news in top_news:
            history.append(news["id"])
        save_history(history)
        
    except Exception as e:
        print(f"❌ Failed to post: {e}")

if __name__ == "__main__":
    process_and_post()

