from kafka import KafkaConsumer
import sys

server = ""
topics = ["news_api"]

def main() -> int:
    if (len(sys.argv) != 1):
        print(f"Usage: {sys.argv[0]}")
        return 1

    consumer = KafkaConsumer(topics=topics, bootstrap_servers=[server])

    for msg in consumer:
        print(msg)

if __name__ == '__main__':
    sys.exit(main())
