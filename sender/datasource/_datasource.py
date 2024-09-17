from datetime import date, datetime, timedelta


class IDatasource:
    def __init__(self, since_date: date = date.today() - timedelta(days=1)) -> None:
        pass

    def get(self) -> dict:
        pass


class INewsDatasource(IDatasource):

    def __init__(self, since_date: date = date.today() - timedelta(days=1)) -> None:
        self.since_date = since_date

    def get(self) -> dict:
        articles = self._get_articles()
        articles = self._filter(articles)
        res = []
        for article in articles:
            obj = {}
            obj["date"] = self._extract_date(article)
            obj["headline"] = self._extract_headline(article)
            obj["content"] = self._extract_content(article)
            obj["image_link"] = self._extract_image_link(article)
            obj["reference_links"] = self._extract_reference_links(article)
            res.append(obj)
        return res

    def _get_articles(self) -> list:
        pass

    def _extract_headline(self, raw: dict) -> str:
        pass

    def _extract_content(self, raw: dict) -> str:
        pass

    def _extract_image_link(self, raw: dict) -> str:
        pass

    def _extract_reference_links(self, raw: dict) -> list:
        pass

    def _extract_date(self, raw: dict) -> str:
        pass

    def _filter(self, articles: list):
        pass
