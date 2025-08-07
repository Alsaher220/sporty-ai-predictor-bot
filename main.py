import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from predict_command import predict

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing in the environment variables")

app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("predict", predict))

if __name__ == "__main__":
    logging.info("Bot is starting...")
    app.run_polling()
