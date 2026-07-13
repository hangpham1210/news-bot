import asyncio

from news.crawler import get_news
from bot.sender import send_news


async def main():

    news = get_news()

    print(f"Lấy được {len(news)} bài.")

    await send_news(news)


if __name__ == "__main__":
    asyncio.run(main())