import base64
import os

import boto3

kms_client = boto3.client("kms")

kms_key_id = "77729b16-a52f-46a5-8e92-454198e50097"
unsubscribe_lambda_url = (
    "https://cfq63ce57k2xekjgvbr4hon5ka0egwgd.lambda-url.us-east-2.on.aws/"
)

recipient = "kanesweet11@gmail.com"

response = kms_client.encrypt(KeyId=kms_key_id, Plaintext=recipient.encode("utf-8"))
ciphertext = response["CiphertextBlob"]

base64_encoded_ciphertext = base64.urlsafe_b64encode(ciphertext).decode("utf-8")

url = unsubscribe_lambda_url + "?user=" + base64_encoded_ciphertext
print(url[:-2])
