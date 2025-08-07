import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from predict_command import predict

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Alive", 200

def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Sporty Score Bot!\n Send /predict Team1 vs Team2"
    )

def main():
    # Start Flask for health check
    Thread(target=run_flask, daemon=True).start()

    # Start Telegram bot
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("predict", predict))
    print("✅ Bot running...")
    telegram_app.run_polling()

if __name__ == "__main__":
    main()
