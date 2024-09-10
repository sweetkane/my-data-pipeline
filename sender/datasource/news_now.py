import os
from datetime import date, timedelta

import requests

from datasource._datasource import INewsDatasource


class NewsNow(INewsDatasource):
    def __init__(self, since_date: date = date.today() - timedelta(days=1)) -> None:
        super().__init__(since_date)
        self.date_key = "date"
        self.date_format = "%Y-%m-%dT%H:%M:%S%z"
        self.url = "https://newsnow.p.rapidapi.com/"
        self.params = {"text": "Top news", "region": "wt-wt", "max_results": 25}
        self.headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
            "X-RapidAPI-Host": "newsnow.p.rapidapi.com",
        }

    def _get_articles(self) -> list:
        response = requests.post(self.url, json=self.params, headers=self.headers)
        if response.status_code != 200:
            print(f"e: {response.status_code}")
            return []
        response = response.json()
        articles = response["news"]
        return articles

    def _extract_headline(self, raw: dict) -> str:
        return raw["title"]

    def _extract_content(self, raw: dict) -> str:
        return raw["body"]

    def _extract_image_link(self, raw: dict) -> str:
        return raw["image"]

    def _extract_reference_links(self, raw: dict) -> [str]:
        return [raw["url"]]
