import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

BOT_USERNAME = "Danachat1_bot"   # بدون @
HF_MODEL = "microsoft/Phi-3-mini-4k-instruct"   # مستقیم بنویس، getenv نباید باشد

def query_huggingface(prompt):
    url = "https://router.huggingface.co/inference"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    payload = {
        "model": HF_MODEL,
        "inputs": prompt,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except:
            return "Response parsing error"

    return f"Error: {response.status_code} - {response.text}"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if f"@{BOT_USERNAME}" in text:
        prompt = text.replace(f"@{BOT_USERNAME}", "").strip()
        result = query_huggingface(prompt)
        await update.message.reply_text(result)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()