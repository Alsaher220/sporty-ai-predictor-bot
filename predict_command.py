import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is missing in the environment variables")

client = OpenAI(api_key=openai_api_key)

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        prompt = " ".join(context.args)
        if not prompt:
            await update.message.reply_text("⚠️ Please provide a match to predict.\nExample:\n`/predict Chelsea vs Real Madrid on Saturday`")
            return

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Predict the outcome of this football match based on stats and recent form: {prompt}"}],
            max_tokens=150,
            temperature=0.7,
        )

        prediction = response.choices[0].message.content
        await update.message.reply_text(f"⚽ Prediction:\n{prediction}")

    except Exception as e:
        logging.error(f"Error in /predict: {e}")
        await update.message.reply_text("⚠️ Something went wrong. Please try again later.")
