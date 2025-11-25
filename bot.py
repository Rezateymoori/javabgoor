import os
import logging
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI
from openai.error import OpenAIError

# ===== تنظیمات Logging =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== متغیرهای محیطی =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # توکن تلگرام
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # کلید Gemini / OpenAI

if not BOT_TOKEN or not OPENAI_API_KEY:
    logger.error("توکن تلگرام یا OpenAI API تنظیم نشده است!")
    exit(1)

# ===== کلاینت Gemini =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== تابع پاسخ به پیام‌ها =====
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message_text = update.message.text
        chat_id = update.message.chat_id

        # فقط پاسخ دادن به گروه‌ها
        if update.message.chat.type not in [Chat.GROUP, Chat.SUPERGROUP]:
            return

        # درخواست به Gemini
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # مدل Gemini
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message_text}
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content
        await context.bot.send_message(chat_id=chat_id, text=answer)

    except OpenAIError as e:
        logger.error(f"خطا در API Gemini: {e}")
        await context.bot.send_message(chat_id=chat_id, text="متاسفم، مشکلی پیش آمد.")
    except Exception as e:
        logger.error(f"خطا عمومی: {e}")

# ===== راه‌اندازی ربات =====
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # فقط پیام‌های متنی
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), reply)
    app.add_handler(text_handler)

    logger.info("ربات Gemini آماده است...")
    app.run_polling()