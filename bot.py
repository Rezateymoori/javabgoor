import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# --------------------------
# تنظیمات توکن‌ها
# --------------------------
BOT_TOKEN = "توکن_ربات_تو " 
OPENAI_API_KEY = "کلید_API_OpenAI_تو" 

client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------
# دستورات پایه
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات هوشمند شما هستم. پیام بدید تا جواب بدم!"
    )

# --------------------------
# پاسخ با هوش مصنوعی
# --------------------------
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user.first_name

    # بررسی نوع چت (دایرکت یا گروه)
    if update.message.chat.type == "private" or f"@{context.bot.username}" in text:
        try:
            # درخواست به OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": text}]
            )

            answer = response.choices[0].message.content
            await update.message.reply_text(answer)

        except Exception as e:
            await update.message.reply_text(f"خطا در دریافت پاسخ: {e}")

# --------------------------
# ساخت اپلیکیشن تلگرام
# --------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("ربات هوشمند آماده است...")
app.run_polling()