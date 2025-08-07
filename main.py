import logging
from flask import Flask
import threading
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# === Set your OpenAI API key ===
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Flask app to prevent Render timeout ===
app = Flask(__name__)

@app.route('/')
def home():
    return "SportyScoreProBot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# === Telegram command: /predict ===
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        question = ' '.join(context.args)
        if not question:
            await update.message.reply_text("⚠️ Please add a match prediction question after /predict.")
            return

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Predict the outcome of this football match with reasoning: {question}"}],
            max_tokens=150
        )

        prediction = response['choices'][0]['message']['content']
        await update.message.reply_text(prediction)

    except Exception as e:
        logging.error(f"Error in /predict: {e}")
        await update.message.reply_text("⚠️ Sorry, there was an error generating the prediction.")

# === Main ===
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Start the Flask server in a separate thread
    threading.Thread(target=run_flask).start()

    # Start the Telegram bot
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    app_bot = ApplicationBuilder().token(telegram_token).build()
    app_bot.add_handler(CommandHandler("predict", predict))

    logging.info("✅ SportyScoreProBot is starting...")
    app_bot.run_polling()
