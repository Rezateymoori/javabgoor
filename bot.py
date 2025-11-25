import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# گرفتن توکن‌ها از Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    raise RuntimeError("لطفاً TELEGRAM_TOKEN و GROQ_API_KEY را در Environment Variables تنظیم کنید.")

# اتصال به Groq
client = Groq(api_key=GROQ_API_KEY)

# Logging
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال است ✔️")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        # درخواست به Groq
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": user_text}
            ]
        )

        bot_reply = completion.choices[0].message["content"]
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text(f"خطا از Groq:\n{e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, chat))
    app.run_polling()

if __name__ == "__main__":
    main()