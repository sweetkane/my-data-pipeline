import json

import boto3
from botocore.exceptions import ClientError

# DynamoDB table
table = boto3.resource("dynamodb").Table("UserEmails")


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
            "body": json.dumps({"message": "Sign-up successful!", "email": email}),
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON in the request body."}),
        }
