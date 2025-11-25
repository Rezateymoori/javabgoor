import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# ====== تنظیمات ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # توکن تلگرام
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")  # کلید Hugging Face
MODEL_ID = "declare-lab/flan-t5-small"  # نمونه مدل سبک و رایگان
API_URL = f"https://router.huggingface.co/api/models/{MODEL_ID}"

# ====== تابع پاسخ‌دهی ======
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    user_message = update.message.text
    bot_username = (await context.bot.get_me()).username

    # بررسی اینکه ربات منشن شده باشد یا پیام ریپلای شده باشد
    if f"@{bot_username}" not in user_message and update.message.reply_to_message is None:
        return  # اگر ربات منشن نشده و پیام ریپلای نیست، نادیده بگیر

    # پاک کردن منشن از متن
    user_message = user_message.replace(f"@{bot_username}", "").strip()

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    payload = {
        "inputs": user_message
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "error" in data:
            answer = "Error from model: " + data["error"]
        elif isinstance(data, list):
            answer = data[0]["generated_text"]
        else:
            answer = str(data)
    except Exception as e:
        answer = f"Error: {e}"

    await update.message.reply_text(answer)

# ====== دستور استارت ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Mention me or reply to me in the group and I'll respond!")

# ====== اجرای ربات ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot is running in group mentions and DMs...")
    app.run_polling()