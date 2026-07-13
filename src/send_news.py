import asyncio

from pipeline import run_pipeline
from bot.sender import send_news



async def main():

    news = run_pipeline()

    # chỉ gửi tin quan trọng
    news = [
        x for x in news
        if x.get("importance", 0) >= 7
    ]


    await send_news(news)



if __name__ == "__main__":

    asyncio.run(main())