import sys
from datetime import date, timedelta
from clients._client import IClient
from clients.email_client import EmailClient

clients: dict[str, type[IClient]] = {
    "email": EmailClient
}

def main() -> int:
    if (len(sys.argv) != 2 or sys.argv[1] not in clients.keys()):
        print(f"Usage: {sys.argv[0]} <client>")
        print("Clients:")
        [print(f"- {option}") for option in clients.keys()]
        return 1

    key = sys.argv[1]

    client = clients[key](date.today()-timedelta(days=1))
    client.post()


if __name__ == '__main__':
    sys.exit(main())
