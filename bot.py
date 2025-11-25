import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_API_KEY = os.environ.get("HF_API_KEY")
MODEL = "TheBloke/vicuna-7B-1.1-HF"  # مدل رایگان Hugging Face

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}
    response = requests.post(f"https://api-inference.huggingface.co/models/{MODEL}", headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        await update.message.reply_text(result[0]['generated_text'])
    else:
        await update.message.reply_text("Error: could not get response.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()