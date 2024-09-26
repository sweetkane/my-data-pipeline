import base64

import boto3

kms_client = boto3.client("kms")
table = boto3.resource("dynamodb").Table("UserEmails")


def get_and_decrypt_email(event):
    query_params = event.get("queryStringParameters", {})
    print("query_params = ", query_params)
    encrypted_email = query_params.get("user")
    print("encrypted email = ", encrypted_email)

    if not encrypted_email:
        raise Exception("No cypher text found in the event...")

    padding = "=" * (4 - len(encrypted_email) % 4)
    encrypted_token_bytes = base64.urlsafe_b64decode(encrypted_email + padding)
    print("encrypted_token_bytes = ", encrypted_token_bytes)
    decrypt_response = kms_client.decrypt(CiphertextBlob=encrypted_token_bytes)
    print("decrypt_response = ", decrypt_response)
    email = decrypt_response["Plaintext"].decode("utf-8")
    print("decrypted email = " + email)
    return email


def lambda_handler(event, context):
    try:
        email = get_and_decrypt_email(event)

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "An error occurred while decrypting the token",
        }
    try:
        table.delete_item(Key={"Email": email})
        # return some html
        html_content = """
        <html>
            <head>
                <title>Subscription Status</title>
            </head>
            <body>
                <h1>You have successfully unsubscribed from Robonews</h1>
            </body>
        </html>
        """

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html_content,
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "An error occurred while deleting the user from the table",
        }
