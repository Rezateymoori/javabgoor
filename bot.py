import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
BOT_USERNAME = os.getenv("Danachat1_bot")  # مثل MySmartBot
HF_MODEL = "declare-lab/flan-t5-small"

def query_huggingface(prompt):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code}"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if f"@{BOT_USERNAME}" in text:
        prompt = text.replace(f"@{BOT_USERNAME}", "").strip()
        response = query_huggingface(prompt)
        await update.message.reply_text(response)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()