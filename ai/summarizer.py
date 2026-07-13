import json
import os

from dotenv import load_dotenv
from google import genai

# Đọc biến môi trường
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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

Chủ đề:
{article.get("topic", "")}

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