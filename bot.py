import os
from genai import Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن‌ها رو از محیط بگیر
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# ساخت کلاینت GenAI
genai_client = Client(api_key=GENAI_API_KEY)

# نمونه هندلر
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات آماده است.")

async def generate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = " ".join(context.args)
    if not user_text:
        await update.message.reply_text("لطفاً متنی برای تولید بفرست.")
        return

    # تولید متن با GenAI
    response = genai_client.generate_text(prompt=user_text)
    await update.message.reply_text(response.text)

# ساخت اپلیکیشن تلگرام
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("say", generate_text))

if __name__ == "__main__":
    print("Bot started...")
    app.run_polling()