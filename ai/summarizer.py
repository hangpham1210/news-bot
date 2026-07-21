import json
import os
import time

from dotenv import load_dotenv
from google import genai

# Đọc biến môi trường
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


HIGH_IMPACT_KEYWORDS = {
    "lãi suất",
    "lạm phát",
    "tỷ giá",
    "ngân hàng",
    "thuế",
    "chính sách",
    "nghị định",
    "xăng dầu",
    "giá vàng",
    "chứng khoán",
    "m&a",
    "sáp nhập",
    "phá sản",
    "thu hồi",
    "đình chỉ",
}

BUSINESS_KEYWORDS = {
    "kinh tế",
    "thị trường",
    "đầu tư",
    "xuất khẩu",
    "doanh thu",
    "lợi nhuận",
    "bán lẻ",
    "retail",
    "siêu thị",
    "tăng giá",
    "giảm giá",
}


def rule_based_importance(article):
    """Chấm điểm 1-10 từ các tín hiệu kinh tế/bán lẻ trong dữ liệu RSS."""

    text = f"{article.get('title', '')} {article.get('content', '')}".lower()
    matched_high_impact = sorted(word for word in HIGH_IMPACT_KEYWORDS if word in text)
    matched_business = sorted(word for word in BUSINESS_KEYWORDS if word in text)

    # Mọi bài có điểm nền 3; tín hiệu ảnh hưởng lớn được ưu tiên cao hơn.
    importance = min(10, 3 + 2 * len(matched_high_impact) + len(matched_business))
    tags = (matched_high_impact + matched_business)[:5]

    return importance, tags


def fallback_summary(article):
    """Dùng dữ liệu RSS và quy tắc khi Gemini không trả kết quả."""

    content = " ".join(article.get("content", "").split())
    if len(content) > 300:
        excerpt = content[:300].rsplit(" ", 1)[0]
    else:
        excerpt = content or article["title"]
    importance, tags = rule_based_importance(article)

    return {
        # Giữ nguyên title RSS trong bài; sender sẽ dùng nó làm tiêu đề Telegram.
        "title": article["title"],
        "summary": [excerpt] if excerpt else [],
        "importance": importance,
        "reason": "Tóm tắt RSS và chấm điểm theo quy tắc vì Gemini không khả dụng.",
        "tags": tags,
    }


def is_service_unavailable(error):
    """True khi Gemini trả lỗi tạm thời 503 có thể retry."""

    message = str(error).lower()
    return "503" in message or "unavailable" in message


def summarize_article(article):
    """
    Tóm tắt 1 bài báo bằng Gemini.
    """

    prompt = f"""
Bạn là một biên tập viên báo chí.

Đọc bài báo dưới đây và trả kết quả DUY NHẤT dưới dạng JSON hợp lệ.

Yêu cầu:

1. summary
- Gồm đúng 3 gạch đầu dòng.
- Mỗi ý tối đa 30 từ.
- Không thêm bình luận.

2. importance
- Điểm từ 1 đến 10.

3. reason
- Một câu giải thích ngắn.

4. tags
- Tối đa 5 từ khóa.

Chỉ trả về JSON.

Ví dụ:

{{
    "summary": [
        "...",
        "...",
        "..."
    ],
    "importance": 8,
    "reason": "...",
    "tags": [
        "...",
        "..."
    ]
}}

====================

Tiêu đề:
{article["title"]}

Nội dung:
{article.get("content", "")}
"""

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    # Xóa markdown nếu Gemini trả về ```json
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        result = json.loads(text)

        article["summary"] = result.get("summary", [])
        article["importance"] = result.get("importance", 0)
        article["reason"] = result.get("reason", "")
        article["tags"] = result.get("tags", [])

    except Exception as e:

        print("Không đọc được JSON từ Gemini:")
        print(text)
        print(e)

        article["summary"] = []
        article["importance"] = 0
        article["reason"] = ""
        article["tags"] = []

    return article


def summarize_with_retry(news):

    max_retries = 3

    # 1 lần gọi đầu + tối đa 3 lần retry khi Gemini trả 503.
    for retry_count in range(max_retries + 1):

        try:
            return summarize_article(news)

        except Exception as error:
            if not is_service_unavailable(error):
                raise

            if retry_count == max_retries:
                print("❌ Gemini 503 sau 3 lần retry → dùng fallback")
                return fallback_summary(news)

            wait_seconds = 2 ** retry_count
            print(
                f"⚠️ Gemini 503. Retry {retry_count + 1}/{max_retries} "
                f"sau {wait_seconds} giây..."
            )
            time.sleep(wait_seconds)
