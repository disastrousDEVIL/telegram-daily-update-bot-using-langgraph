import os
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv
from graph import graph

load_dotenv()
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")

def handle_message(update, context):
    user_input=update.message.text

    result=graph.invoke({"input": user_input})
    output=result["output"]
    update.message.reply_text(output)

def main():
    updater=Updater(BOT_TOKEN)
    dp=updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("LangGraph bot running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    