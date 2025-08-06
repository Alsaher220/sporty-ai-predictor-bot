import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from predict_command import predict

BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Sporty Score Bot!\n\n"
        "Use /predict Team1 vs Team2 to get match predictions.\n"
        "Example: /predict Arsenal vs Chelsea"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))

print("✅ Bot is running...")
app.run_polling()
