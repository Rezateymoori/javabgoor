import os
import google.generativeai as genai
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# دریافت توکن‌ها از محیط
TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN or not GEMINI_KEY:
    raise RuntimeError("لطفاً TELEGRAM_TOKEN و GEMINI_API_KEY را در Environment Variables ست کنید.")

# پیکربندی Gemini
genai.configure(api_key=GEMINI_KEY)

# پیدا کردن خودکار اولین مدل Gemini
def get_available_model():
    models = genai.list_models()
    print("لیست مدل‌ها:", [m.name for m in models])  # برای دیباگ
    for m in models:
        if "gemini" in m.name.lower():
            return m.name
    raise RuntimeError("مدل Gemini پیدا نشد. لطفاً API Key خود را بررسی کنید.")

# انتخاب مدل
model_name = get_available_model()
model = genai.GenerativeModel(model_name)
print(f"✅ از مدل استفاده می‌شود: {model_name}")

# هندلر پیام‌های تلگرام
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text

        # تولید متن با مدل انتخاب‌شده
        response = model.generate_text(user_text)

        # پاسخ به کاربر
        await update.message.reply_text(response.output_text)

    except Exception as e:
        await update.message.reply_text(f"❌ خطا از Gemini:\n{e}")

# ایجاد اپلیکیشن تلگرام و اضافه کردن هندلر
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# شروع polling
app.run_polling()