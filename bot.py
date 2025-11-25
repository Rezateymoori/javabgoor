import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# از Railway یا لوکال می‌آید
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# اسم ربات را مستقیم بنویس (بدون @)
BOT_USERNAME = "Danachat1_bot"

# مدل سبک
HF_MODEL = "google/flan-t5-small"

def query_huggingface(prompt):
    url = f"https://router.huggingface.co/v1/inference"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    payload = {
        "model": HF_MODEL,
        "inputs": prompt,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # اگر توی پیام تگ شده بود
    if f"@{BOT_USERNAME}" in text:
        prompt = text.replace(f"@{BOT_USERNAME}", "").strip()
        response = query_huggingface(prompt)
        await update.message.reply_text(response)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()