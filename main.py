from email import message
from fastapi import FastAPI,Request
import os
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters
import requests
from graph import graph


load_dotenv()
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")

TELEGRAM_API_URL=f"https://api.telegram.org/bot{BOT_TOKEN}"
app=FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data=await request.json()

    message=data.get("message",{})
    chat_id=message.get("chat",{}).get("id")
    text=message.get("text")
    
    if not text or not chat_id:
        return {"status": "ignored"}
    
    result=graph.invoke({"input": text})
    output=result["output"]


    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={"chat_id": chat_id, "text": output})
    print("LangGraph received:", output)

    return {"status": "ok"}
