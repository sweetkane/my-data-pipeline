import json
from datetime import date, timedelta

from clients._client import IClient


class PrintClient(IClient):
    def __init__(self) -> None:
        super().__init__()

    def post(self, data: dict):
        try:
            print(json.dumps(data))
        except:
            print(data)
