import json
from pathlib import Path

READY_FILE = Path("data/ready_news.json")


def save_ready_news(news):
    READY_FILE.parent.mkdir(exist_ok=True)

    with open(
        READY_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            news,
            f,
            ensure_ascii=False,
            indent=2
        )


def load_ready_news():

    if not READY_FILE.exists():
        return []

    with open(
        READY_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)