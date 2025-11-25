import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters  # <-- توجه کنید
import genai

# تنظیمات API
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

genai.configure(api_key=GENAI_API_KEY)

def get_available_model():
    models = genai.list_models()
    print("لیست مدل‌ها:", [m.name for m in models])
    for m in models:
        if m.name.startswith("models/gemini") and "-pro" in m.name:
            return m.name
    for m in models:
        if m.name.startswith("models/gemini"):
            return m.name
    raise RuntimeError("مدل Gemini پیدا نشد. لطفاً API Key خود را بررسی کنید.")

MODEL_NAME = get_available_model()
print("مدل انتخاب شده:", MODEL_NAME)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من بات شما هستم. پیام خود را بفرستید تا جواب بدهم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = genai.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": user_text}]
        )
        answer = response.output_text
    except Exception as e:
        answer = f"خطا در پاسخ‌دهی: {e}"
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("بات شروع شد...")
    app.run_polling()

if __name__ == "__main__":
    main()