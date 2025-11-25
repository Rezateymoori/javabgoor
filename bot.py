# bot.py
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# ========================
# Configuration
# ========================
BOT_TOKEN = "BOT_TOKEN"  # replace with your BotFather token
HF_MODEL = "mistralai/mistral-small"   # free Hugging Face model
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_API_KEY = os.environ.get("HF_API_KEY")  # set this in environment

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# ========================
# Reply function
# ========================
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return

    payload = {
        "inputs": user_message,
        "parameters": {"max_new_tokens": 150}
    }

    try:
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            answer = data[0]["generated_text"]
        else:
            answer = "Sorry, no response was generated."
    except Exception as e:
        answer = f"Error: {e}"

    await update.message.reply_text(answer)

# ========================
# Start command
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am a reply bot. Send me a message and I will answer.")

# ========================
# Bot setup
# ========================
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot is running...")
app.run_polling()