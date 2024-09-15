import os
from datetime import date, timedelta

from datasource._datasource import INewsDatasource
from newsapi import NewsApiClient


class NewsAPI(INewsDatasource):
    def __init__(self, since_date: date = date.today() - timedelta(days=1)) -> None:
        super().__init__(since_date)
        self.date_key = "publishedAt"
        self.date_format = "%Y-%m-%dT%H:%M:%SZ"
        news_api_key = os.environ.get("NEWS_API_KEY")
        self.api_client = NewsApiClient(news_api_key)

    def _get_articles(self) -> list:
        res = self.api_client.get_top_headlines()
        articles = res["articles"]
        return articles

    def _extract_headline(self, raw: dict) -> str:
        return raw["title"]

    def _extract_content(self, raw: dict) -> str:
        return f"Description: {raw['description']}\n\nContent: {raw['content']}"

    def _extract_image_link(self, raw: dict) -> str:
        return raw["urlToImage"]

    def _extract_reference_links(self, raw: dict):
        return raw["url"]
