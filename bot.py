import os
import google.generativeai as genai
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN or not GEMINI_KEY:
    raise RuntimeError("لطفاً TELEGRAM_TOKEN و GEMINI_API_KEY را در Environment Variables ست کنید.")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = model.generate_content(user_text)

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"❌ خطا از Gemini:\n{e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()