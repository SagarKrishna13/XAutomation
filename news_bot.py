import os
import sys
import json
import time
import requests
import tweepy
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
NEWSDATA_API_KEY = os.environ.get("NEWSDATA_API_KEY")
X_API_KEY        = os.environ.get("X_API_KEY")
X_API_SECRET     = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN   = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET  = os.environ.get("X_ACCESS_SECRET")

HISTORY_FILE   = "posted_history.json"
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
        "category": "top",
    }

    print(f"[INFO] Fetching news from NewsData.io ...")
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"[INFO] NewsData API status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "success":
            print(f"[ERROR] NewsData API returned error: {data}")
            return []

        results = data.get("results", [])
        print(f"[INFO] NewsData returned {len(results)} articles.")
        return results

    except Exception as e:
        print(f"[ERROR] Exception during news fetch: {e}")
        return []


def process_and_post():
    # --- Validate secrets ---
    missing = [k for k, v in {
        "NEWSDATA_API_KEY": NEWSDATA_API_KEY,
        "X_API_KEY":        X_API_KEY,
        "X_API_SECRET":     X_API_SECRET,
        "X_ACCESS_TOKEN":   X_ACCESS_TOKEN,
        "X_ACCESS_SECRET":  X_ACCESS_SECRET,
    }.items() if not v]

    if missing:
        print(f"[ERROR] Missing secrets: {', '.join(missing)}")
        print("[ERROR] Please set them in GitHub → Settings → Secrets and variables → Actions")
        sys.exit(1)

    print("[INFO] All secrets are present ✅")

    # --- Authenticate with X (Twitter) v2 ---
    print("[INFO] Authenticating with X API v2 ...")
    client_v2 = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
    )

    # --- Verify credentials by checking rate limit / making a dummy safe call ---
    try:
        me = client_v2.get_me()
        if me and me.data:
            print(f"[INFO] Authenticated as: @{me.data.username} (ID: {me.data.id}) ✅")
        else:
            print("[WARN] get_me() returned no data — credentials may be read-only or invalid.")
    except tweepy.errors.Forbidden as e:
        print(f"[ERROR] Authentication succeeded but app lacks READ permission: {e}")
        sys.exit(1)
    except tweepy.errors.Unauthorized as e:
        print(f"[ERROR] Unauthorized — API keys are incorrect or revoked: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[WARN] Could not verify identity (non-fatal): {e}")

    # --- Fetch news ---
    history  = load_history()
    print(f"[INFO] Loaded {len(history)} previously posted article IDs from history.")
    articles = fetch_news()

    if not articles:
        print("[ERROR] No articles returned from news API. Exiting.")
        sys.exit(1)

    # --- Filter duplicates and pick top 3 ---
    top_news = []
    for article in articles:
        article_id = article.get("article_id") or article.get("link")
        if not article_id:
            continue
        if article_id in history:
            continue
        title = article.get("title", "").strip()
        if title and len(top_news) < 3:
            top_news.append({"id": article_id, "title": title})

    if not top_news:
        print("[WARN] No new unique news to post — all fetched articles were already in history.")
        print("[INFO] Consider clearing posted_history.json if this persists.")
        # Exit 0 (not an error, just nothing new today)
        sys.exit(0)

    print(f"[INFO] Found {len(top_news)} new article(s) to post.")

    # --- Build tweet ---
    tweet_lines = ["📰 Top Breaking News:\n"]
    for i, news in enumerate(top_news, 1):
        title = news["title"]
        if len(title) > 80:
            title = title[:77] + "..."
        tweet_lines.append(f"{i}. {title}")

    tweet_text = "\n".join(tweet_lines)

    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."

    print(f"\n[INFO] Tweet to post ({len(tweet_text)} chars):\n{'-'*40}")
    print(tweet_text)
    print("-" * 40)

    # --- Post tweet ---
    try:
        response = client_v2.create_tweet(text=tweet_text)
        tweet_id = response.data["id"]
        print(f"\n[SUCCESS] ✅ Posted: https://x.com/i/status/{tweet_id}")

        # Save history
        for news in top_news:
            history.append(news["id"])
        save_history(history)
        print(f"[INFO] Saved {len(top_news)} article IDs to history.")

    except tweepy.errors.Forbidden as e:
        print(f"\n[ERROR] ❌ 403 Forbidden — Your X app likely has READ-ONLY permissions.")
        print("[ERROR] Fix: Go to developer.twitter.com → Your App → Settings → App permissions → change to 'Read and Write'")
        print(f"[ERROR] Full error: {e}")
        sys.exit(1)
    except tweepy.errors.TooManyRequests as e:
        print(f"\n[ERROR] ❌ 429 Too Many Requests — Rate limit hit.")
        print(f"[ERROR] Full error: {e}")
        sys.exit(1)
    except tweepy.errors.Unauthorized as e:
        print(f"\n[ERROR] ❌ 401 Unauthorized — Access tokens invalid or expired.")
        print("[ERROR] Fix: Regenerate your Access Token and Secret on developer.twitter.com")
        print(f"[ERROR] Full error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] ❌ Failed to post tweet: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    process_and_post()
