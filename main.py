import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from genai import GenAI

# ======= گرفتن توکن‌ها از Environment =======
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")

# ======= تنظیم GenAI =======
genai = GenAI(api_key=GENAI_API_KEY)

# ======= فرمان /start =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من بات هوشمند شما هستم. هر چیزی بپرسید!")

# ======= فرمان /ask =======
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("لطفاً یک سوال بعد از /ask بنویسید!")
        return
    
    # پاسخ از GenAI
    try:
        response = genai.generate(question)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"خطا در گرفتن پاسخ: {e}")

# ======= اجرای بات =======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # افزودن Handlerها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    
    print("بات در حال اجراست...")
    app.run_polling()