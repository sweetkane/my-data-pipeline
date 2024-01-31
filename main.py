from datetime import date, timedelta
from datasource._datasource import IDatasource
from datasource.news_api import NewsAPI
from datasource.connexun_news import ConnexunNews
from datasource.news_now import NewsNow
from datetime import date, timedelta
from clients._client import IClient
from clients.email_client import EmailClient


datasources: dict[str, type[IDatasource]] = {
    "news_api": NewsAPI,
    "connexun_news": ConnexunNews,
    "news_now": NewsNow
}

clients: dict[str, type[IClient]] = {
    "email": EmailClient
}

def handler(event, context):
    datasource_keys = event["datasources"]
    client_keys = event["clients"]

    data = []
    for key in datasource_keys:
        datasource = datasources[key](date.today()-timedelta(days=1))
        data += datasource.get()

    for key in client_keys:
        client = clients[key]()
        client.post(data)

    return {
        "data_len": len(data)
    }


# if __name__ == '__main__':
#     sys.exit(
#         handler(
#             {
#                 "datasources": ["connexun_news", "news_now"],
#                 "clients": ["email"]
#             },
#             {}
#         )
#     )
