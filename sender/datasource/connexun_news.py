import os
from datetime import date, timedelta

import requests

from datasource._datasource import INewsDatasource


class ConnexunNews(INewsDatasource):
    def __init__(self, since_date: date = date.today() - timedelta(days=1)) -> None:
        super().__init__(since_date)
        self.date_key = "PublishedOn"
        self.date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.url = "https://news67.p.rapidapi.com/v2/feed"
        self.params = {"batchSize": "30", "languages": "en"}
        self.headers = {
            "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
            "X-RapidAPI-Host": "news67.p.rapidapi.com",
        }

    def _get_articles(self) -> list:
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            print(f"e: {response.status_code}")
            return []
        response = response.json()
        articles = response["news"]
        return articles

    def _extract_headline(self, raw: dict) -> str:
        return raw["Title"]

    def _extract_content(self, raw: dict) -> str:
        return f"Description: {raw['Description']}\n\nSummary: {raw['Summary']}"

    def _extract_image_link(self, raw: dict) -> str:
        return raw["Image"]

    def _extract_reference_links(self, raw: dict) -> [str]:
        return [raw["Url"]]
