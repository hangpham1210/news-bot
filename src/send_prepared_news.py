import sys
import os
import asyncio

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)

from src.storage import load_ready_news
from bot.sender import send_news


async def main():

    news = load_ready_news()

    print(f"Ready news: {len(news)}")

    await send_news(news)


if __name__ == "__main__":
    asyncio.run(main())