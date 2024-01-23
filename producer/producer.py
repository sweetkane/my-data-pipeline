from datetime import date
from datasource.datasource import IDatasource
import json

server = ""
class Producer:
    def __init__(self, topic: str, datasource: IDatasource) -> None:
        self.topic = topic
        self.datasource = datasource


    def send_since(self, since_date: date):
        data = self.datasource.get_since(since_date)
        encoded_data = json.dumps(data).encode()


