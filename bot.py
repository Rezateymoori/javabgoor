import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import genai

# تنظیمات API
GENAI_API_KEY = os.getenv("GENAI_API_KEY")  # یا مستقیم قرار بدهید
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # توکن بات تلگرام

genai.configure(api_key=GENAI_API_KEY)

def get_available_model():
    models = genai.list_models()
    print("لیست مدل‌ها:", [m.name for m in models])  # برای دیباگ
    # انتخاب اولین مدل Gemini-Pro موجود
    for m in models:
        if m.name.startswith("models/gemini") and "-pro" in m.name:
            return m.name
    # fallback: مدل flash یا دیگر مدل‌های Gemini
    for m in models:
        if m.name.startswith("models/gemini"):
            return m.name
    raise RuntimeError("مدل Gemini پیدا نشد. لطفاً API Key خود را بررسی کنید.")

MODEL_NAME = get_available_model()
print("مدل انتخاب شده:", MODEL_NAME)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! من بات شما هستم. پیام خود را بفرستید تا جواب بدهم.")

def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    # درخواست به مدل Gemini
    try:
        response = genai.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": user_text}]
        )
        answer = response.output_text
    except Exception as e:
        answer = f"خطا در پاسخ‌دهی: {e}"
    update.message.reply_text(answer)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("بات شروع شد...")
    updater.idle()

if __name__ == "__main__":
    main()