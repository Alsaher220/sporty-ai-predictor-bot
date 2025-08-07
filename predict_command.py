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
        await update.message.reply_text(f"⚠️ Error: {e}")
