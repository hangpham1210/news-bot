from datetime import datetime


def parse_news(item: dict) -> dict:
    """
    Chuẩn hóa dữ liệu RSS
    """

    return {

        "source": item.get("source", ""),

        "title": item.get("title", "").strip(),

        # RSS summary dùng làm nội dung ban đầu
        "content": item.get("summary", "").strip(),

        # topic mặc định
        "topic": item.get("category", ""),

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