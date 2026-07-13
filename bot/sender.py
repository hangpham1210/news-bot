from telegram import Bot
from telegram.constants import ParseMode

from dotenv import load_dotenv
import os


load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


if not BOT_TOKEN:
    raise ValueError("❌ Thiếu TELEGRAM_BOT_TOKEN trong file .env")


if not CHAT_ID:
    raise ValueError("❌ Thiếu TELEGRAM_CHAT_ID trong file .env")



async def send_news(news):

    """
    Gửi danh sách tin lên Telegram.
    """

    bot = Bot(token=BOT_TOKEN)


    if not news:

        await bot.send_message(
            chat_id=CHAT_ID,
            text="📭 Hôm nay không có tin mới."
        )

        return



    message = (
        "📰 <b>RETAIL NEWS UPDATE</b>\n\n"
    )



    for idx, article in enumerate(news, 1):


        importance = article.get(
            "importance",
            0
        )


        topic = article.get(
            "topic",
            "Khác"
        )


        summary = article.get(
            "summary",
            []
        )


        tags = article.get(
            "tags",
            []
        )


        message += (
            f"<b>{idx}. {article.get('title')}</b>\n"
            f"📌 Chủ đề: {topic}\n"
            f"⭐ Importance: {importance}/10\n\n"
        )



        if summary:

            for s in summary:

                message += f"• {s}\n"


        if tags:

            message += (
                "\n🏷 Tags: "
                + ", ".join(tags)
                + "\n"
            )


        message += (
            f"\n🔗 {article.get('link')}\n\n"
            "--------------------\n\n"
        )



    await bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )