from datetime import datetime
from html import unescape


def parse_news(item: dict) -> dict:
    """
    Chuẩn hóa dữ liệu RSS
    """

    title = unescape(
        item.get("title", "").strip()
    )

    content = unescape(
        item.get("content")
        or item.get("summary", "").strip()
    )

    topic = unescape(
        item.get("category", "")
    )

    return {

        "source": item.get("source", ""),

        "title": title,

        # Dùng toàn văn do crawler lấy được; chỉ dùng RSS summary khi không có.
        "content": content,

        # topic mặc định
        "topic": topic,

        "summary": "",

        "published": normalize_date(
            item.get("published")
        ),

        "category": "",

        "importance": 0,

        "reason": "",

        "tags": [],

        "link": item.get("link", "")
    }


def normalize_date(date_value):

    if not date_value:
        return None

    return str(date_value)