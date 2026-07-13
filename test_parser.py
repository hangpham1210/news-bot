from news.crawler import crawl_all
from news.parser import parse_news


news = crawl_all()

parsed = [
    parse_news(x)
    for x in news
]


for item in parsed[:5]:
    print("----------------")
    print(item)