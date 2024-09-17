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
print(f"ciphertext = \n{ciphertext}\n")
encrypted_email = base64.urlsafe_b64encode(ciphertext).decode("utf-8")[:-1]
print(f"encrypted_email = \n{encrypted_email}\n")

url = unsubscribe_lambda_url + "?user=" + encrypted_email
# print(url)

encrypted_token_bytes = base64.urlsafe_b64decode(encrypted_email + "=")
print(f"encrypted_token_bytes = \n{encrypted_token_bytes}\n")
decrypt_response = kms_client.decrypt(CiphertextBlob=encrypted_token_bytes)
print("decrypt_response = ", decrypt_response)
email = decrypt_response["Plaintext"].decode("utf-8")
print("decrypted email = " + email)
