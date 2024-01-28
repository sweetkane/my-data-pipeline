from datetime import date, timedelta

class IClient:
    def __init__(self, since_date: date = date.today()-timedelta(days=1)) -> None:
        pass

    def post(self):
        data = self._gather_data()
        payload = self._synthesize(data)
        self._send(payload)

    def _gather_data(self) -> dict:
        pass

    def _synthesize(self, data: dict) -> dict:
        pass

    def _send(self, payload: dict):
        pass
