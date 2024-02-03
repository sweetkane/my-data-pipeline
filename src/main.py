from datasource._datasource import IDatasource
from datasource.news_api import NewsAPI
from datasource.connexun_news import ConnexunNews
from datasource.news_now import NewsNow
from transforms._transform import ITransform
from transforms.news_synthesizer import NewsSynthesizer
from clients._client import IClient
from clients.email_client import EmailClient
from clients.print_client import PrintClient
import sys

datasources: dict[str, type[IDatasource]] = {
    "news_api": NewsAPI,
    "connexun_news": ConnexunNews,
    "news_now": NewsNow
}

transforms: dict[str, type[ITransform]] = {
    "news_synthesizer": NewsSynthesizer
}

clients: dict[str, type[IClient]] = {
    "email": EmailClient,
    "print": PrintClient
}

def handler(event, context):
    datasource_keys = event["datasources"]
    transform_keys = event["transforms"]
    client_keys = event["clients"]

    data = []
    for key in datasource_keys:
        datasource = datasources[key]()
        data += datasource.get()

    for key in transform_keys:
        transform = transforms[key]()
        data = transform.transform(data)

    for key in client_keys:
        client = clients[key]()
        client.post(data)


if __name__ == '__main__':
    sys.exit(
        handler(
            {
                "datasources": ["news_now"],
                "transforms": ["news_synthesizer"],
                "clients": ["print", "email"]
            },
            {}
        )
    )
