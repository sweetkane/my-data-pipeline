import base64
import json
import os

import boto3
from botocore.exceptions import ClientError

# DynamoDB table
ses_client = boto3.client("ses")
kms_client = boto3.client("kms")
sender = "robonews@kanesweet.com"


def get_subscribe_link(recipient: str) -> str:
    kms_key_id = os.environ["KMS_KEY_ID"]
    subscribe_lambda_url = os.environ["SUBSCRIBE_LAMBDA_URL"]

    response = kms_client.encrypt(KeyId=kms_key_id, Plaintext=recipient.encode("utf-8"))
    ciphertext = response["CiphertextBlob"]

    base64_encoded_ciphertext = base64.urlsafe_b64encode(ciphertext)
    utf_cypher = base64_encoded_ciphertext.decode("utf-8")[:-1]

    return subscribe_lambda_url + "?user=" + utf_cypher


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
                        <p>Click <a href="{get_subscribe_link(email)}">here</a> to confirm your email!</p>
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
