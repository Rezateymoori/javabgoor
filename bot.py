import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from genai import GenAI

# توکن‌های خودت را از متغیرهای محیطی بگیر
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")

# ساخت کلاینت GenAI با نسخه 1.x
client = GenAI(api_key=GENAI_API_KEY)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات شما هستم. هر چیزی بنویسید من جواب میدم.")

# پاسخ به پیام‌ها
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # تولید پاسخ با GenAI
    response = client.generate_text(user_message)
    
    # ارسال پاسخ به کاربر
    await update.message.reply_text(response)

# ساخت اپلیکیشن تلگرام
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# اضافه کردن هندلرها
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

# اجرای ربات
if __name__ == "__main__":
    print("ربات آماده است!")
    app.run_polling()