from datetime import date, timedelta
from datasource._datasource import IDatasource
from datasource.news_api import NewsAPI
from datasource.connexun_news import ConnexunNews
from datasource.news_now import NewsNow
import sys

datasources: dict[str, type[IDatasource]] = {
    "news_api": NewsAPI,
    "connexun_news": ConnexunNews,
    "news_now": NewsNow
}

def main() -> int:
    if (len(sys.argv) != 2 or sys.argv[1] not in datasources.keys()):
        print(f"Usage: {sys.argv[0]} <datasource>")
        print("Datasources:")
        [print(f"- {option}") for option in datasources.keys()]
        return 1

    key = sys.argv[1]

    datasource = datasources[key](date.today()-timedelta(days=1))
    arts = datasource.get()

    import json

    with open('res.json', 'a') as fp:
            json.dump(arts, fp)

if __name__ == '__main__':
    sys.exit(main())
