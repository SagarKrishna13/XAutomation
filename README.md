# X News Automation Bot 🤖📰

Automatically posts top 3 breaking news headlines to X (Twitter) every 2 hours using GitHub Actions.

**Live Repo:** https://github.com/pjob9456/XAutomation

## ✅ Features

- Posts **1 combined tweet** with top 3 news headlines every 2 hours
- Fetches from NewsData.io API
- Duplicate detection (won't re-post same articles)
- **X Free tier compliant**: Only 12 tweets/day (limit is 50)
- **24/7 automation** via GitHub Actions (no laptop needed!)

## Tweet Format

```
📰 Top Breaking News:

1. First headline here...
2. Second headline here...
3. Third headline here...
```

---

## 📅 Schedule

The bot runs automatically every 2 hours starting at 2:00 AM IST:

| IST Time | UTC Time |
|----------|----------|
| 2:00 AM | 20:30 UTC |
| 4:00 AM | 22:30 UTC |
| 6:00 AM | 00:30 UTC |
| 8:00 AM | 02:30 UTC |
| 10:00 AM | 04:30 UTC |
| 12:00 PM | 06:30 UTC |
| 2:00 PM | 08:30 UTC |
| 4:00 PM | 10:30 UTC |
| 6:00 PM | 12:30 UTC |
| 8:00 PM | 14:30 UTC |
| 10:00 PM | 16:30 UTC |
| 12:00 AM | 18:30 UTC |

---

## ⚙️ How to Change the Schedule

Edit `.github/workflows/news_bot.yml` and modify the `cron` lines:

```yaml
on:
  schedule:
    - cron: '30 20,22 * * *'           # 2 AM and 4 AM IST
    - cron: '30 0,2,4,6,8,10,12,14,16,18 * * *'  # Rest of the day
```

**Cron format:** `minute hour day month weekday`

### Examples:
| Schedule | Cron Expression |
|----------|-----------------|
| Every hour | `0 * * * *` |
| Every 3 hours | `0 */3 * * *` |
| Every 6 hours | `0 */6 * * *` |
| Once daily at 9 AM IST | `30 3 * * *` |

**IST to UTC:** Subtract 5 hours 30 minutes from IST time

---

## X Free Tier Compliance

| Metric | Value |
|--------|-------|
| Tweets per run | **1** |
| Runs per day | **12** |
| Total tweets/day | **12** |
| X Free limit | **50** |
| **Status** | ✅ Safe |

---

## Files

| File | Description |
|------|-------------|
| `news_bot.py` | Main bot - posts top 3 news in one tweet |
| `api_client.py` | Test news API separately |
| `posted_history.json` | Tracks posted articles |
| `.github/workflows/news_bot.yml` | GitHub Actions schedule |

## Manual Trigger

Go to [Actions tab](https://github.com/pjob9456/XAutomation/actions) → "Post News to X" → "Run workflow"

## License

MIT
