# 🤖 XAutomation - End-to-End Project Explanation

This document explains exactly how the **XAutomation** bot works, step-by-step, in simple terms.

---

## 🚀 **1. The Big Picture**

This project is a **News Bot** that:
1.  **Wakes up** automatically every 2 hours.
2.  **Checks** for the latest breaking news in India.
3.  **Filtrs** out old news so it doesn't repeat itself.
4.  **Posts** a summary of the top 3 headlines to X (Twitter).
5.  **Goes back to sleep** to save resources.

It runs entirely on **GitHub Actions**, which means it runs in the cloud for free. You do **not** need to keep your computer on.

---

## 🔄 **2. The Workflow (Step-by-Step)**

Here is what happens every time the bot runs:

### **Step 1: The Alarm Clock (GitHub Actions)** ⏰
**File:** `.github/workflows/news_schedule.yml`

Just like you set an alarm on your phone, we set a "Schedule" on GitHub.
-   **The Code:** `cron: '0 */2 * * *'`
-   **What it means:** "Run this code at minute 0 past every 2nd hour."
-   **Result:** GitHub automatically starts a virtual computer (Ubuntu), installs Python, and runs your script.

### **Step 2: Fetching the News** 🌍
**File:** `news_bot.py` (Function: `fetch_news()`)

Once the script starts, it needs to find news. It talks to **NewsData.io**, a service that collects news from the internet.
-   **It asks:** "Give me the latest TOP news from INDIA in ENGLISH."
-   **The API Key:** It uses a secret password (`NEWSDATA_API_KEY`) to prove it's allowed to ask.
-   **Result:** The bot gets a list of articles (Titles, Links, Images).

### **Step 3: Checking for Duplicates** 🕵️‍♂️
**File:** `news_bot.py` & `posted_history.json`

The bot doesn't want to be annoying and post the same thing twice.
-   **It looks at:** `posted_history.json` (a file that keeps a list of news IDs we already posted).
-   **The Logic:**
    -   "Have I posted this article ID before?"
    -   **Yes?** Skip it. ❌
    -   **No?** Keep it! ✅
-   It picks the **top 3** new articles that passed this check.

### **Step 4: Writing the Tweet** ✍️
**File:** `news_bot.py` (Function: `process_and_post()`)

Now it formats the text nicely for X (Twitter).
-   It creates a list like:
    ```
    📰 Top Breaking News:

    1. [Headline 1]
    2. [Headline 2]
    3. [Headline 3]
    ```
-   **Character Limit:** Twitter only allows 280 characters. The bot checks the length and cuts off text (adds "...") if it's too long, so the tweet doesn't fail.

### **Step 5: Posting to X (Twitter)** 📨
**File:** `news_bot.py`

Finally, it sends the text to Twitter.
-   **Authentication:** It uses 4 secret keys (API Key, Secret, Access Token, Secret) to log in to your account securely.
-   **Action:** It sends the tweet.
-   **Success?** If Twitter says "OK", the bot saves the IDs of those 3 articles into `posted_history.json` so it remembers for next time.

### **Step 6: Saving Memory** 💾
**File:** `news_bot.py` (Function: `save_history()`)

-   The bot updates `posted_history.json` with the new articles.
-   **Important:** If the list gets too big (over 500 items), it deletes the oldest ones to keep the file small and fast.
-   *(Optional Step in GitHub Actions)*: The workflow commits this updated JSON file back to your repository so the memory is saved for the next run.

---

## 📂 **3. File Explanations**

| File Name | Purpose |
| :--- | :--- |
| **`news_bot.py`** | **The Brain.** This contains all the logic: fetching news, checking history, formatting text, and posting to Twitter. |
| **`api_client.py`** | **The Tester.** A simple script just to test if the News API is working correctly without posting anything to Twitter. Use this for debugging. |
| **`posted_history.json`** | **The Memory.** A simple database file that lists the IDs of news we have already posted. |
| **`.github/workflows/news_schedule.yml`** | **The Schedule.** The configuration file that tells GitHub WHEN to run your bot. |
| **`requirements.txt`** | **The Toolkit.** A list of Python libraries (like `tweepy`, `requests`) the bot needs to install to work. |
| **`.env`** | **The Secrets.** (Local only) Stores your passwords on your computer. On GitHub, these are stored in "Secrets & Variables". |

---

## � **4. API Architecture & Security**

This section explains the technical "type" of connections we use and how we keep them safe.

### **API Type: REST API**
We use **REST (Representational State Transfer)** APIs for both NewsData.io and X (Twitter).
*   **How it talks:** It's like visiting a website, but instead of getting HTML (webpages), we exchange **JSON** (data).
*   **Example (NewsData):** We send a `GET` request to `https://newsdata.io/...` and it replies with a JSON list of news.
*   **Example (Twitter):** We send a `POST` request to `https://api.twitter.com/...` with our tweet text in the JSON body.

### **Security: How we stay safe 🛡️**

We use **"Secrets Management"** to ensure your account is never hacked.

#### **1. Environment Variables (The Golden Rule)**
*   **Checking the code:** You will see `os.environ.get("X_API_KEY")` in `news_bot.py`.
*   **What this means:** The code **NEVER** contains the actual password. It only asks the computer "Do you know the password?".
*   **Why?** If you share your code, no one sees your keys.

#### **2. GitHub Secrets (The Vault)**
*   On GitHub, we store keys in **Settings > Secrets and variables > Actions**.
*   These are **Encrypted at Rest**. Once you save them, even YOU cannot see them again. You can only update or delete them.
*   GitHub injects them into the bot **only for the few seconds** it is running, then wipes them.

#### **3. OAuth 1.0a (Twitter Authentication)**
*   We don't just use a username and password. We use **OAuth Tokens**.
*   **Consumer Key/Secret:** Identifies "Who is the App?" (XAutomation Bot).
*   **Access Token/Secret:** Identifies "Who is the User?" (Your Account).
*   **Benefit:** If the bot key is stolen, you can revoke just the bot's access without changing your actual Twitter password.

#### **4. HTTPS (Encryption)**
*   All communication between GitHub, NewsData, and Twitter happens over **HTTPS**.
*   This means the data is encrypted **in transit**, so no one can intercept your keys or news data while it travels across the internet.

---

## 🔗 **5. CI/CD & Automation**

This project uses **GitHub Actions** as its CI/CD system.

### **How the Pipeline Works**
1.  **Trigger 🎯**: The `cron` schedule (every 2 hours) wakes up the pipeline.
2.  **Spin Up 🖥️**: GitHub creates a temporary virtual machine.
3.  **Inject Secrets 🔑**: GitHub securely unlocks the vault and gives the keys to the temporary machine.
4.  **Run Logic ⚡**: It executes `news_bot.py`.
5.  **Commit Memory 💾**: It saves `posted_history.json` back to the repo so the bot isn't "amnesiac" next time it runs.
