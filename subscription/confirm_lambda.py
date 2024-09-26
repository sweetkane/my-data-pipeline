import base64
import json
import os
import urllib.parse
import urllib.request

import boto3

# DynamoDB table
kms_client = boto3.client("kms")
sender = "robonews@kanesweet.com"


def send_email(sender, recipient, subject, html):
    url = "https://api.mailgun.net/v3/kanesweet.com/messages"

    data = urllib.parse.urlencode(
        {
            "from": f"RoboNews <{sender}>",
            "to": recipient,
            "subject": subject,
            "html": html,
        }
    ).encode()

    api_key = os.environ["MAILGUN_API_KEY"]
    auth = f"api:{api_key}".encode("ascii")
    auth_header = base64.b64encode(auth).decode("ascii")

    request = urllib.request.Request(url, data=data)
    request.add_header("Authorization", f"Basic {auth_header}")

    try:
        with urllib.request.urlopen(request) as response:
            print(f"Sent email to: {recipient}")
            return response.read().decode()
    except urllib.error.HTTPError as e:
        raise Exception(f"Error: {e.read().decode()}")


def get_subscribe_link(recipient: str) -> str:
    kms_key_id = os.environ["KMS_KEY_ID"]
    subscribe_lambda_url = os.environ["SUBSCRIBE_LAMBDA_URL"]

    response = kms_client.encrypt(KeyId=kms_key_id, Plaintext=recipient.encode("utf-8"))
    ciphertext = response["CiphertextBlob"]

    base64_encoded_ciphertext = base64.urlsafe_b64encode(ciphertext)
    utf_cypher = base64_encoded_ciphertext.decode("utf-8").rstrip("=")

    link = subscribe_lambda_url + "?user=" + utf_cypher
    print(f"Created: {link}")
    return link


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

    html = f"""
        <html>
            <body>
            <h1>Thanks for subscribing to Robonews! 🤖</h1>
            <hr>
            <p>Click <a href="{get_subscribe_link(email)}">here</a> to confirm your email!</p>
            <br></br>
            <a href="https://github.com/sweetkane/robonews">GitHub</a>
            </body>
        </html>
        """

    send_email(sender, email, "Robonews Email Confirmation", html)
