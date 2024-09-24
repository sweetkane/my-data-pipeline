import base64
import json

import boto3
from botocore.exceptions import ClientError

# DynamoDB table
table = boto3.resource("dynamodb").Table("UserEmails")
kms_client = boto3.client("kms")


def get_and_decrypt_email(event):
    query_params = event.get("queryStringParameters", {})
    print("query_params = ", query_params)
    encrypted_email = query_params.get("user")
    print("encrypted email = ", encrypted_email)

    if not encrypted_email:
        raise Exception("No cypher text found in the event...")

    encrypted_token_bytes = base64.urlsafe_b64decode(encrypted_email + "=")
    print("encrypted_token_bytes = ", encrypted_token_bytes)
    decrypt_response = kms_client.decrypt(CiphertextBlob=encrypted_token_bytes)
    print("decrypt_response = ", decrypt_response)
    email = decrypt_response["Plaintext"].decode("utf-8")
    print("decrypted email = " + email)
    return email


response_html = """
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Subscription Status</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f0f0f0;
    }

    .text-container {
      background-color: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      width: 300px;
      text-align: center;
    }

    .description-text {
      color: #4a4a4a; /* Dark grey */
      font-size: 16px; /* Adjust as needed */
      line-height: 1.6; /* Improves readability */
      font-family: Arial, sans-serif; /* Choose a clean font */
    }
  </style>
</head>
<body>
<div>
  <div class="text-container">
    <h2>You have successfully subscribed to RoboNews! </h2>
    <p class="description-text">Check your inbox for new content every week 🤖</p>
  </div>
</div>
</body>
</html>
"""


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        email = get_and_decrypt_email(event)

        try:
            table.put_item(Item={"Email": email})
        except ClientError as e:
            print(f"Error adding item: {e.response['Error']['Message']}")

            return {
                "statusCode": 500,
                "body": json.dumps({"message": "Failed to add email."}),
            }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": response_html,
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON in the request body."}),
        }
