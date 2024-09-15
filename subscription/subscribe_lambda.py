import json

import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")
# Specify your table name
table = dynamodb.Table("UserEmails")


def lambda_handler(event, context):
    # Log the incoming event for debugging
    print("Received event:", json.dumps(event))

    try:
        # Body is expected to be in the event object as a string
        body = json.loads(event.get("body", "{}"))

        email = body.get("email", None)

        if not email:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "Email is required in the request body."}
                ),
            }

        # add to dynamodb
        try:
            # Add an item to the table
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
