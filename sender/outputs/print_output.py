import json
from datetime import date, timedelta

from outputs._output import IOutput


class PrintOutput(IOutput):
    def __init__(self) -> None:
        super().__init__()

    def post(self, content):
        print(content)
