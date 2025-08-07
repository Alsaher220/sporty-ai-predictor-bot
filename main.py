import logging
import threading
import os
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler
from predict_command import predict

# === Logging ===
logging.basicConfig(level=logging.INFO)

# === Check environment variable for Telegram Bot Token ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("⚠️ TELEGRAM_BOT_TOKEN environment variable is missing!")

# === Flask app for Render uptime ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ SportyScoreProBot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# === Start Telegram Bot ===
def run_telegram_bot():
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("predict", predict))
    logging.info("🚀 SportyScoreProBot is starting...")
    app_bot.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_telegram_bot()
