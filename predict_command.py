from telegram import Update
from telegram.ext import ContextTypes
import logging
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# === /predict command ===
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = ' '.join(context.args)
        if not user_input:
            await update.message.reply_text("⚠️ Please add a match to predict. Example: `/predict Arsenal vs Chelsea`")
            return

        # Basic AI response (you can improve this with actual logic)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Predict this match: {user_input}"}],
            max_tokens=150
        )

        prediction = response['choices'][0]['message']['content']
        await update.message.reply_text(prediction)

    except Exception as e:
        logging.error(f"❌ Error in /predict: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Try again later.")
