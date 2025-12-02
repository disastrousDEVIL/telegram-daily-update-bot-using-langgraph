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
* When a message arrives, it is processed with LangGraph
* Response is sent directly using the Telegram API
* Works offline, but **your PC must stay running**

---

## 📂 Project Structure

```
main.py                 # FastAPI webhook server for Render deployment
graph.py                # LangGraph logic
bot_polling_backup.py   # Polling version (runs locally)
requirements.txt        # Dependencies
.gitignore              # Ignore env, venv, cache
.env                    # Local environment variables (ignored)
.env.example            # Template showing required variables
```

---

## 🔑 Environment Variables

The bot needs the following variables, defined in `.env` or your OS environment:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_key
```

These are documented in `.env.example`.

### Important:

If you run locally and your system already has `OPENAI_API_KEY` set, you do not need it inside `.env`.

If deploying on Render, **set both variables in Render's Environment tab**.

---

# ▶️ Running the Polling Version (local machine)

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the polling bot:

```
python bot_polling_backup.py
```

3. Behavior:

* Keeps checking Telegram for new messages
* Laptop must stay on
* Simple option but not suitable for cloud/production

---

# ▶️ Running the Webhook Version (FastAPI, local)

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Start FastAPI:

```
uvicorn main:app --reload
```

3. Test webhook (PowerShell):

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/webhook" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"message": {"chat": {"id": 123}, "text": "hello"}}'
```

If you receive `200 OK`, the webhook is working.

---

# ☁️ Deploying Webhook Mode on Render (recommended)

1. Push the project to GitHub
2. Create a **New Web Service** on Render
3. Set:

```
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 8000
```

4. Add environment variables:

```
TELEGRAM_BOT_TOKEN=xxxxx
OPENAI_API_KEY=xxxxx
```

5. Set Telegram webhook:

```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_RENDER_URL>/webhook
```

Your bot will now run 24×7 in the cloud.

---

# 📌 Summary: When to use which method?

### **Polling Bot**

* Runs on laptop
* No deployment needed
* Simple but requires your system to stay on

### **Webhook Bot (FastAPI)**

* Runs in the cloud
* Best for production
* Always online
* Zero maintenance