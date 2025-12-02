# 📝 Telegram Daily Update Bot (FastAPI + LangGraph + Polling Version)

This bot converts short daily notes into clean, professional daily updates.
It supports two modes:

1. **Polling Bot (runs on your local machine)**
2. **Webhook Bot (FastAPI server, deployable on Render for 24×7 uptime)**

The bot uses:

* FastAPI (for webhook mode)
* LangGraph (for message transformation)
* OpenAI models (gpt-5-mini / gpt-5-nano)

---

## ⚙️ How It Works

### **Webhook Mode**

* Telegram sends updates → `/webhook` (FastAPI)
* FastAPI forwards text → LangGraph
* LangGraph generates polished daily updates
* Bot responds instantly on Telegram

### **Polling Mode**

* Python script continuously polls Telegram
* When a message arrives → it’s processed with LangGraph
* Response is sent back directly via Telegram API
* Works offline, but **requires your PC to stay on**

---

## 📂 Project Structure

```
main.py                 # FastAPI webhook server for Render deployment
graph.py                # LangGraph logic
bot_polling_backup.py   # Polling version (runs locally)
requirements.txt        # Dependencies
.gitignore              # Ignore env, venv, cache
.env (local)            # Environment variables (ignored by git)
```

---

## 🔑 Environment Variables

Both versions require:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_key
```

### Important

Your system already has `OPENAI_API_KEY` set in OS-level environment variables.
Others will need to set it manually on their server (Render, Railway, etc.).

Add this note in the code:

```python
# NOTE:
# OPENAI_API_KEY is sourced from system environment variables.
# If deploying on a server (Render), add it in the Environment tab.
```

---

# ▶️ Running the Polling Version (local machine)

Use this when you want to run the bot **without FastAPI**, just a simple script.

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the polling bot

```
python bot_polling_backup.py
```

### 3. How it behaves

* This method keeps checking Telegram for new messages
* Your laptop must stay ON
* No deployment required
* Simpler but not suitable for production

---

# ▶️ Running the Webhook Version (FastAPI, local)

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Start FastAPI

```
uvicorn main:app --reload
```

### 3. Test the webhook (PowerShell)

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/webhook" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"message": {"chat": {"id": 123}, "text": "hello"}}'
```

If you see `200 OK` → your webhook server works.

---

# ☁️ Deploying Webhook Mode on Render (recommended)

### 1. Push code to GitHub

### 2. Create a **New Web Service** on Render

### 3. Configure:

```
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Add Environment Variables in Render:

```
TELEGRAM_BOT_TOKEN=xxxx
OPENAI_API_KEY=xxxx
```

### 5. Set your Telegram webhook:

```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_RENDER_URL>/webhook
```

Your bot now runs 24×7, even when your computer is off.

---

# 📌 Summary: When to use which method?

### **Polling Bot**

* Runs on your laptop
* Easy to test
* No deployment
* Must stay running
* Not ideal long-term

### **Webhook Bot (FastAPI)**

* Runs in the cloud (Render)
* Designed for production
* Lightning fast
* Zero maintenance
* Your laptop stays off

