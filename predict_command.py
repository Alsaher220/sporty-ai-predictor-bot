from telegram import Update
from telegram.ext import ContextTypes
import logging
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text
        prompt = f"Based on current stats, predict the outcome of this football match: {message}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )

        prediction = response.choices[0].message["content"]
        await update.message.reply_text(f"⚽ Prediction:\n{prediction}")

    except Exception as e:
        logging.error(f"Error in /predict: {e}")
        await update.message.reply_text(f"⚠️ Error: {e}")
