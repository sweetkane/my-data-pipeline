import os

import boto3

# Initialize the KMS client
kms_client = boto3.client("kms")


def lambda_handler(event, context):
    # Retrieve the encrypted token from the event
    encrypted_email = event.get("user")

    if not encrypted_email:
        return {"statusCode": 400, "body": "No encryptedToken found in the event"}

    # Decode the encrypted token from base64 (assuming it's base64 encoded)
    encrypted_token_bytes = bytes.fromhex(encrypted_email)

    try:
        # Decrypt the token using KMS
        decrypt_response = kms_client.decrypt(CiphertextBlob=encrypted_token_bytes)

        # Get the decrypted value
        decrypted_value = decrypt_response["Plaintext"].decode("utf-8")

        # Store the decrypted value in the variable 'email'
        email = decrypted_value

        return {"statusCode": 200, "body": {"email": email}}

    except kms_client.exceptions.KMSInvalidStateException as e:
        print(f"KMS Invalid State Exception: {e}")
        return {"statusCode": 500, "body": "KMS Invalid State Exception"}
    except kms_client.exceptions.KMSAccessDeniedException as e:
        print(f"KMS Access Denied Exception: {e}")
        return {"statusCode": 403, "body": "Access Denied to KMS Key"}
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "An error occurred while decrypting the token",
        }
