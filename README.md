# X News Automation Bot 🤖📰

Automatically posts top 3 breaking news headlines to X (Twitter) every 2 hours using GitHub Actions.

## Features

- ✅ Posts **1 combined tweet** with top 3 news headlines every 2 hours
- ✅ Fetches from NewsData.io API
- ✅ Duplicate detection (won't re-post same articles)
- ✅ **X Free tier compliant**: Only 12 tweets/day (limit is 50)
- ✅ **24/7 automation** via GitHub Actions (no laptop needed)

## Tweet Format

```
📰 Top Breaking News:

1. First headline here...
2. Second headline here...
3. Third headline here...
```

---

## 🚀 GitHub Setup (24/7 Automation)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/XAutomation.git
git branch -M main
git push -u origin main
```

### Step 2: Add Secrets

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add these 5 secrets:

| Secret Name | Value |
|-------------|-------|
| `NEWSDATA_API_KEY` | `pub_b993b1572ec14b6b876078d0e0bf64e8` |
| `X_API_KEY` | Your X API Key |
| `X_API_SECRET` | Your X API Secret |
| `X_ACCESS_TOKEN` | Your Access Token |
| `X_ACCESS_SECRET` | Your Access Token Secret |

### Step 3: Enable Workflow

1. Go to **Actions** tab in your repo
2. Click **"I understand my workflows, go ahead and enable them"**
3. The bot will now run automatically every 2 hours!

---

## X Free Tier Compliance

| Metric | Value |
|--------|-------|
| Tweets per run | **1** (single combined post) |
| Runs per day | **12** (every 2 hours) |
| Total tweets/day | **12** |
| X Free limit | **50** |
| **Status** | ✅ Well within limits |

---

## Files

| File | Description |
|------|-------------|
| `news_bot.py` | Main bot - posts top 3 news in one tweet |
| `api_client.py` | Test news API separately |
| `posted_history.json` | Tracks posted articles |
| `.github/workflows/news_bot.yml` | GitHub Actions config |

## Manual Run

```bash
# Set environment variables first, then:
python news_bot.py
```

## License

MIT
