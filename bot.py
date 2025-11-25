import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ---------- تنظیمات ----------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # توکن ربات تلگرام
HF_API_KEY = os.environ.get("HF_API_KEY")  # کلید Hugging Face
MODEL = "TheBloke/guanaco-7B-HF"  # مدل رایگان سبک
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# ---------- تابع پاسخ‌دهی ----------
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    payload = {
        "inputs": user_text,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=HEADERS,
            json=payload,
            timeout=60  # زمان انتظار بیشتر
        )
        print("Status code:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                text = data[0]["generated_text"]
            else:
                text = str(data)
        else:
            text = f"Error {response.status_code}: {response.text}"

    except Exception as e:
        text = f"Exception: {str(e)}"

    await update.message.reply_text(text)

# ---------- ساخت ربات ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot is running...")
app.run_polling()