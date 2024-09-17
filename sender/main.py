import sys

from datasource._datasource import IDatasource
from datasource.nyt import Nyt
from outputs._output import IOutput
from outputs.email_output import EmailOutput
from outputs.print_output import PrintOutput
from transforms._transform import ITransform
from transforms.news_summarizer import NewsSummarizer

datasources: dict[str, type[IDatasource]] = {"nyt": Nyt}

transforms: dict[str, type[ITransform]] = {"news_summarizer": NewsSummarizer}

outputs: dict[str, type[IOutput]] = {"email": EmailOutput, "print": PrintOutput}


def lambda_handler(event, context):
    datasource_keys = event["datasources"]
    transform_key = event["transform"]
    output_keys = event["outputs"]

    data = []
    try:
        for key in datasource_keys:
            datasource = datasources[key]()
            data += datasource.get()
    except Exception as e:
        print(
            f"""
        Failed to get from datasource
        -----------------------------
        e: {e}
        """
        )
        return {
            "statusCode": 500,
            "body": e,
        }
    try:
        transform = transforms[transform_key]()
        content = transform.apply(data)
    except Exception as e:
        print(
            f"""
        Failed to apply transform
        --------------------------
        e: {e}
        """
        )
        return {
            "statusCode": 500,
            "body": e,
        }
    try:
        for key in output_keys:
            output = outputs[key]()
            output.post(content)
    except Exception as e:
        print(
            f"""
        Failed to post to output
        ------------------------
        e: {e}
        """
        )
        return {
            "statusCode": 500,
            "body": e,
        }

    print("Finished successfully")
    return "Finished successfully"


if __name__ == "__main__":
    sys.exit(
        lambda_handler(
            {
                "datasources": ["nyt"],
                "transform": "news_summarizer",
                "outputs": ["print", "email"],
            },
            {},
        )
    )
