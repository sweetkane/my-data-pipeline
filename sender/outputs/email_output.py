import base64
import os
import urllib
from datetime import date

import boto3
from outputs._output import IOutput


class EmailOutput(IOutput):
    def __init__(self) -> None:
        super().__init__()
        self.subject = f"🤖RoboNews🤖: {date.today().strftime('%a, %b %-d %Y')}"
        self.title = "Good Morning!\n"
        self.subtitle = "Here's your 🤖RoboNews🤖 for the week..."

        self.user_emails_table = boto3.resource("dynamodb").Table("UserEmails")
        self.ses_client = boto3.client("ses")
        self.kms_client = boto3.client("kms")

    def post(self, content: str):
        """
        data should be a dict with
        - KEY = Subtitle
        - VALUE = Content for that subtitle
        """
        for recipient in self._get_recipients():
            self._send_email(
                sender="robonews@kanesweet.com",
                recipient=recipient,
                subject=self.subject,
                html=self._get_body(content, recipient),
            )

    def _get_recipients(self):
        try:
            response = self.user_emails_table.scan()
            data = response.get("Items", [])

            # Extract and print the emails
            emails = [item["Email"] for item in data]
            return emails
        except Exception as e:
            raise e

    def _send_email(self, sender, recipient, subject, html):
        url = "https://api.mailgun.net/v3/kanesweet.com/messages"

        data = urllib.parse.urlencode(
            {
                "from": f"RoboNews <{sender}>",
                "to": recipient,
                "subject": subject,
                "html": html,
            }
        ).encode()

        api_key = os.environ["MAILGUN_API_KEY"]
        auth = f"api:{api_key}".encode("ascii")
        auth_header = base64.b64encode(auth).decode("ascii")

        request = urllib.request.Request(url, data=data)
        request.add_header("Authorization", f"Basic {auth_header}")

        try:
            with urllib.request.urlopen(request) as response:
                return response.read().decode()
        except urllib.error.HTTPError as e:
            raise Exception(f"Error: {e.read().decode()}")

    def _get_body(self, content: str, recipient: str):
        html = f"""
        <html>
        <head></head>
        <body>
        <h1>{self.title}</h1>
        <div>{self.subtitle}</div>
        <br></br>
        <hr>
        <p>{content}</p>
        <br></br>
        <div>That's all for now... Have a great week!</div>
        <br></br>
        <a href={self._get_unsubscribe_link(recipient)}>Unsubscribe</a> |
        <a href="https://github.com/sweetkane/robonews">GitHub</a>
        </body>
        </html>
        """
        return html

    def _get_unsubscribe_link(self, recipient: str) -> str:
        kms_key_id = os.environ["KMS_KEY_ID"]
        unsubscribe_lambda_url = os.environ["UNSUBSCRIBE_LAMBDA_URL"]

        response = self.kms_client.encrypt(
            KeyId=kms_key_id, Plaintext=recipient.encode("utf-8")
        )
        ciphertext = response["CiphertextBlob"]

        base64_encoded_ciphertext = base64.urlsafe_b64encode(ciphertext)
        utf_cypher = base64_encoded_ciphertext.decode("utf-8").rstrip("=")

        return unsubscribe_lambda_url + "?user=" + utf_cypher
