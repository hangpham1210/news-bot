import asyncio
from collections import defaultdict

from pipeline import run_pipeline
from bot.sender import send_news


# ==========================
# Cấu hình
# ==========================
TOP_NEWS_PER_SOURCE = 2


async def main():

    news = run_pipeline()

    print(f"Pipeline trả về: {len(news)} bài")

    # ==========================
    # Nhóm theo nguồn báo
    # ==========================
    grouped = defaultdict(list)

    for article in news:
        source = article.get("source", "Unknown")
        grouped[source].append(article)

    # ==========================
    # Lấy Top N mỗi nguồn
    # ==========================
    selected_news = []

    for source, articles in grouped.items():

        articles.sort(
            key=lambda x: x.get("importance", 0),
            reverse=True
        )

        top_articles = articles[:TOP_NEWS_PER_SOURCE]

        print(f"{source}: gửi {len(top_articles)} bài")

        selected_news.extend(top_articles)

    # ==========================
    # Sắp xếp lại toàn bộ để bài quan trọng nhất lên đầu Telegram
    # ==========================
    selected_news.sort(
        key=lambda x: x.get("importance", 0),
        reverse=True
    )

    print(f"Sẽ gửi: {len(selected_news)} bài")

    await send_news(selected_news)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("✅ Pipeline completed")
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")