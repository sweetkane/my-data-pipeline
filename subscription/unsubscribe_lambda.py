import base64

import boto3

kms_client = boto3.client("kms")
table = boto3.resource("dynamodb").Table("UserEmails")


def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters", {})
        encrypted_email = query_params.get("user")

        print("encrypted email = ", encrypted_email)

        if not encrypted_email:
            return {
                "statusCode": 400,
                "body": "No encryptedToken found in the event...",
            }

        encrypted_token_bytes = base64.urlsafe_b64decode(encrypted_email + "==")
        decrypt_response = kms_client.decrypt(CiphertextBlob=encrypted_token_bytes)
        decrypted_value = decrypt_response["Plaintext"].decode("utf-8")
        email = decrypted_value
        print("decoded email = " + email)
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "An error occurred while decrypting the token",
        }
    try:
        table.delete_item(Key={"Email": email})
        # return some html
        return {"statusCode": 200, "body": {"email": email}}
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "An error occurred while deleting the user from the table",
        }
