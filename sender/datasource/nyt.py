from datetime import date, timedelta

import feedparser
from datasource._datasource import INewsDatasource


class Nyt(INewsDatasource):

    def __init__(self, since_date: date = date.today() - timedelta(days=1)) -> None:
        self.since_date = since_date
        self.rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"

    def _get_articles(self) -> list:
        feed = feedparser.parse(self.rss_url)
        return feed.entries

    def _extract_headline(self, raw: dict) -> str:
        return raw.title

    def _extract_content(self, raw: dict) -> str:
        return raw.description

    def _extract_image_link(self, raw: dict) -> str:
        if "media_content" in raw:
            return raw.media_content[0]["url"]
        else:
            return ""

    def _extract_reference_links(self, raw: dict) -> list:
        return raw.link

    def _extract_date(self, raw: dict) -> str:
        return raw.published

    def _filter(self, articles: list):
        res = []
        for article in articles:
            if self._contains_category_ai(article):
                res.append(article)
        return res

    def _contains_category_ai(self, article: dict):
        for tag in article.tags:
            if tag.term == "Artificial Intelligence":
                return True
        return False
