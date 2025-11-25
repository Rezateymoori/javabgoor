# bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import genai

# ست کردن API Key برای GenAI
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.api_key = GENAI_API_KEY

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات هوشمند هستم. یه چیزی بهم بگو!")

# پاسخ به پیام‌های متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # ساخت پاسخ با GenAI
    response = genai.Text.create(
        model="xlarge",
        prompt=user_text
    )

    await update.message.reply_text(response.text)

if __name__ == "__main__":
    # توکن ربات تلگرام
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    # ساخت اپلیکیشن تلگرام
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # اجرای ربات
    app.run_polling()