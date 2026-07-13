from src.database.history import init_db, save_news, is_exist


init_db()


test = {

    "title":"Test news",

    "link":"https://test.com/article1",

    "source":"Test",

    "category":"Retail",

    "importance":8,

    "summary":"Demo"

}


print(
    "Before:",
    is_exist(test["link"])
)


save_news(test)


print(
    "After:",
    is_exist(test["link"])
)