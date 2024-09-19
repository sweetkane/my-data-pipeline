import json
import os

import boto3
from botocore.exceptions import ClientError

# DynamoDB table
ses_client = boto3.client("ses")
kms_client = boto3.client("kms")
sender = "robonews@kanesweet.com"


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        body = json.loads(event.get("body", "{}"))

        email = body.get("email", None)

        if not email:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "Email is required in the request body."}
                ),
            }
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON in the request body."}),
        }

    ses_client.send_email(
        Destination={"ToAddresses": [email]},
        Message={
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": f"""
                    <html>
                        <body>
                        <h1>Thanks for subscribing to Robonews!</h1>
                        <hr>
                        <p>Click <a href="{os.environ["SUBSCRIBE_LAMBDA_URL"]}?user={email}">here</a> to confirm your email!</p>
                        <br></br>
                        <a href="https://github.com/sweetkane/robonews">GitHub</a>
                        </body>
                    </html>
                    """,
                },
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": "Robonews Email Confirmation",
            },
        },
        Source=sender,
    )
