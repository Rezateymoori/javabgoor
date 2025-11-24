# ============================
# Telegram DeepSeek Bot (Railway)
# Bot: @Javabgoo_gptbot
# ============================

import os
import aiohttp
from telegram import Update, MessageEntity
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

# ---------------------------
# گرفتن توکن‌ها از Environment Variables
# ---------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

if not TELEGRAM_TOKEN or not DEEPSEEK_API_KEY:
    raise RuntimeError("لطفاً TELEGRAM_TOKEN و DEEPSEEK_API_KEY را در Environment Variables تنظیم کنید.")

DEEPSEEK_MODEL = "deepseek-chat"

# ---------------------------
# تابع تماس با DeepSeek
# ---------------------------
async def ask_deepseek(prompt: str) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except:
                return f"خطا در پاسخ DeepSeek:\n{data}"

# ---------------------------
# بررسی منشن شدن ربات
# ---------------------------
def is_mentioned(update: Update, bot_username: str) -> bool:
    msg = update.message
    if not msg or not msg.text:
        return False

    # بررسی ریپلای به ربات
    if msg.reply_to_message and msg.reply_to_message.from_user.username == bot_username:
        return True

    # بررسی entities
    entities = msg.entities or []
    for ent in entities:
        if ent.type == MessageEntity.MENTION:
            start, end = ent.offset, ent.offset + ent.length
            mention = msg.text[start:end]
            if mention.lower() == f"@{bot_username.lower()}":
                return True

    return False

# ---------------------------
# هندلر پیام‌ها
# ---------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    me = await bot.get_me()
    bot_username = me.username

    msg = update.message
    text = msg.text

    if not is_mentioned(update, bot_username):
        return

    await msg.chat.send_action("typing")
    prompt = f"User said: {text}\nRespond as a helpful assistant."
    reply = await ask_deepseek(prompt)
    await msg.reply_text(reply)

# ---------------------------
# اجرای ربات
# ---------------------------
if __name__ == "__main__":
    print("🚀 Bot is running... @Javabgoo_gptbot")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()