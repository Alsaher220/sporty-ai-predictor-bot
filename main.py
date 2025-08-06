import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from predict_command import predict  # This file will contain your AI prediction logic

# Load your Telegram bot token securely from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Sporty AI Predictor Bot!\n\n"
        "Use /predict Team1 vs Team2 to get match predictions.\n"
        "Example: /predict Arsenal vs Chelsea"
    )

# Initialize the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))  # Handles AI prediction

# Run the bot
print("✅ Bot is running...")
app.run_polling()
