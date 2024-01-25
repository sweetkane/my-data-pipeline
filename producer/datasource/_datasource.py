from datetime import date, datetime, timedelta

class INewsDatasource:
    def get_since(self, since_date: date = date.today()-timedelta(days=1)) -> dict:
        self.since_date = since_date
        articles = self._get_articles()
        articles = self._filter_date(articles)
        res = []
        for article in articles:
            obj = {}
            obj["date"] = self._extract_datetime(article).date().strftime("%Y-%m-%d")
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

    def _extract_reference_links(self, raw: dict) -> [str]:
        pass

    def _extract_datetime(self, raw: dict) -> datetime:
        article_datetime = raw[self.date_key]
        article_datetime = datetime.strptime(article_datetime, self.date_format)
        return article_datetime

    def _filter_date(self, articles: [dict]):
        to_remove = []
        for i in range(len(articles)):
            article_datetime = self._extract_datetime(articles[i])
            if article_datetime.date() < self.since_date:
                to_remove.append(i)
        for i in reversed(to_remove):
            articles = articles[:i] + articles[i+1:]
        return articles
