import base64
import os

import boto3

kms_client = boto3.client("kms")
table = boto3.resource("dynamodb").Table("UserEmails")


def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters", {})

        print("qsp = ", query_params)
        encrypted_email = query_params.get("user") + "=="

        if not encrypted_email:
            return {
                "statusCode": 400,
                "body": "No encryptedToken found in the event...",
            }

        encrypted_token_bytes = base64.urlsafe_b64decode(encrypted_email)
        decrypt_response = kms_client.decrypt(CiphertextBlob=encrypted_token_bytes)
        decrypted_value = decrypt_response["Plaintext"].decode("utf-8")
        email = decrypted_value
        print("decoded email = " + email)

        table.delete_item(
            Key={
                "primary_key_name": key_value  # Replace 'primary_key_name' with your table's primary key
            }
        )
        # return some html
        return {"statusCode": 200, "body": {"email": email}}

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "An error occurred while decrypting the token",
        }
