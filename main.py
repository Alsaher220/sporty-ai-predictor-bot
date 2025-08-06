import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from predict_command import predict

# Load your Telegram Bot Token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Sporty Score Bot!\n\n"
        "Send /predict Team1 vs Team2 to get a smart AI prediction!\n\n"
        "Example: /predict Arsenal vs Chelsea"
    )

# Build and run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    
    print("✅ Sporty Score Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
