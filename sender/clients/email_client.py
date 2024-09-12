import os
from datetime import date

import boto3
from botocore.exceptions import ClientError
from clients._client import IClient


class EmailClient(IClient):
    def __init__(self) -> None:
        super().__init__()
        self.subject = f"🤖RoboNews🤖: {date.today().strftime('%a, %b %-d %Y')}"
        self.title = "Good Morning!\n"
        self.subtitle = "Here's your 🤖RoboNews🤖 for the day..."

        self.dynamodb = boto3.resource("dynamodb")
        self.userEmailsTable = self.dynamodb.Table("UserEmails")

    def post(self, data: dict):
        """
        data should be a dict with
        - KEY = Subtitle
        - VALUE = Content for that subtitle
        """
        self._send_email(
            sender="robonews@kanesweet.com",
            recipients=self._get_recipients(),
            subject=self.subject,
            body_html=self._to_html(data),
            aws_region=os.environ["AWS_DEFAULT_REGION"],
        )

    def _get_recipients(self):
        try:
            response = self.userEmailsTable.scan()
            data = response.get("Items", [])

            # Extract and print the emails
            emails = [item["Email"] for item in data]
            return emails
        except Exception as e:
            raise e

    def _send_email(self, sender, recipients, subject, body_html, aws_region):
        # Create a new SES resource and specify a region.
        client = boto3.client("ses", region_name=aws_region)

        # Try to send the email.
        try:
            response = client.send_email(
                Destination={"ToAddresses": recipients},
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
        except ClientError as e:
            print(e.response["Error"]["Message"])
            raise e
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])

    def _to_html(self, data: dict):
        html = f"""
        <html>
        <head></head>
        <body>
        <h1>{self.title}</h1>
        <div>{self.subtitle}</div>
        <br></br>
        <hr>
        """
        for key in data.keys():
            html += f"<h2>{key}</h2>\n"
            html += f"<p>{data[key]}</p>\n"
        html += """
        <hr>
        <br></br>
        <div>That's all... Have a great day!</div>
        <br></br>
        <a href="https://github.com/sweetkane/robonews">GitHub</a>
        </body>
        </html>
        """
        return html
