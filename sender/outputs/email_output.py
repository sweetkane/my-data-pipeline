import base64
import os
from datetime import date

import boto3
from outputs._output import IOutput


class EmailOutput(IOutput):
    def __init__(self) -> None:
        super().__init__()
        self.subject = f"🤖RoboNews🤖: {date.today().strftime('%a, %b %-d %Y')}"
        self.title = "Good Morning!\n"
        self.subtitle = "Here's your 🤖RoboNews🤖 for the day..."

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
                body_html=self._get_body(content, recipient),
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

    def _send_email(self, sender, recipient, subject, body_html):
        # Create a new SES resource and specify a region.

        # Try to send the email.

        # Todo add an unsubscribe link with encrypted email
        try:
            response = self.ses_client.send_email(
                Destination={"ToAddresses": [recipient]},
                Message={
                    "Body": {
                        "Html": {
                            "Charset": "UTF-8",
                            "Data": body_html,
                        },
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": subject,
                    },
                },
                Source=sender,
            )
        except Exception as e:
            print(e.response["Error"]["Message"])
            raise e
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])

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
        <div>That's all... Have a great day!</div>
        <br></br>
        <a href={self._get_unsubscribe_link(recipient)}>Unsubscribe</a>
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

        base64_encoded_ciphertext = base64.urlsafe_b64encode(ciphertext).decode(
            "utf-8"
        )[:-2]

        return unsubscribe_lambda_url + "?user=" + base64_encoded_ciphertext
