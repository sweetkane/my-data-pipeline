import json

import boto3
from botocore.exceptions import ClientError

# DynamoDB table
table = boto3.resource("dynamodb").Table("UserEmails")


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        query_params = event.get("queryStringParameters", {})
        print("query_params = ", query_params)
        email = query_params.get("user")

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

        html_content = """
        <html>
            <head>
                <title>Subscription Status</title>
            </head>
            <body>
                <h1>You have successfully subscribed to Robonews!</h1>
                <p>Expect new content every Monday morning :)</p>
            </body>
        </html>
        """

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html_content,
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON in the request body."}),
        }
