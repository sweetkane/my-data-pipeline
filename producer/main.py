from datetime import date, timedelta
from datasource.datasource import IDatasource
from datasource.news_api import NewsAPI
from producer.producer import Producer
import sys

datasources: dict[str, type(IDatasource)] = {
    "news_api": NewsAPI
}

def main() -> int:
    if (len(sys.argv) != 2 or sys.argv[1] not in datasources.keys()):
        print(f"Usage: {sys.argv[0]} <datasource>")
        print("Datasources:")
        [print(f"- {option}") for option in datasources.keys()]
        return 1

    key = sys.argv[1]

    datasource = datasources[key]()
    producer = Producer(topic=key, datasource=datasource)
    producer.send_since(date.today()-timedelta(days=1))

if __name__ == '__main__':
    sys.exit(main())
