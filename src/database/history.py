import sqlite3
from datetime import datetime
import os
import json


DB_PATH = "data/news_history.db"


def get_connection():

    os.makedirs("data", exist_ok=True)

    return sqlite3.connect(DB_PATH)



def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        link TEXT UNIQUE,

        source TEXT,

        category TEXT,

        importance INTEGER,

        summary TEXT,

        tags TEXT,

        created_at TEXT,

        sent INTEGER DEFAULT 0

    )
    """)

    conn.commit()
    conn.close()



def is_exist(link):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM news_history
        WHERE link = ?
        """,
        (link,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None



def save_news(news):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO news_history
        (
            title,
            link,
            source,
            category,
            importance,
            summary,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,
    (
        news["title"],
        news["link"],
        news.get("source"),
        news.get("category"),
        news.get("importance"),

        json.dumps(
            news.get("summary", []),
            ensure_ascii=False
        ),

        datetime.now().isoformat()
    )
    )

    conn.commit()
    conn.close()