from datetime import date, datetime
from datasource.datasource import IDatasource
from newsapi import NewsApiClient
import os



class NewsAPI(IDatasource):
    def __init__(self) -> None:
        news_api_key = os.environ.get('NEWS_API_KEY')
        self.api_client = NewsApiClient(news_api_key)


    def get_since(self, since_date: date) -> dict:
        res = self.api_client.get_top_headlines()
        articles = res['articles']
        to_remove = []
        for i in range(len(articles)):
            article_date = articles[i]["publishedAt"]
            article_date = datetime.strptime(article_date, "%Y-%m-%dT%H:%M:%SZ")
            if article_date.date() < since_date:
                to_remove.append(i)
        for i in reversed(to_remove):
            articles = articles[:i] + articles[i+1:]
        return {'data': articles}

