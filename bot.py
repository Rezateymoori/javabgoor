import os
from groq import Groq
from telegram.ext import Application, MessageHandler, filters

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not GROQ_API_KEY or not TELEGRAM_TOKEN:
    raise RuntimeError("لطفاً GROQ_API_KEY و TELEGRAM_TOKEN را ست کنید.")

client = Groq(api_key=GROQ_API_KEY)

async def chat(update, context):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": user_text}]
        )

        answer = response.choices[0].message["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"❌ خطای Groq:\n{e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, chat))
    app.run_polling()

if __name__ == "__main__":
    main()