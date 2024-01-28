from datetime import date, timedelta
import boto3
from botocore.exceptions import ClientError
from consumer.clients.synthesizers.email_synthesizer import EmailSynthesizer
from _client import IClient
import os

class EmailClient(IClient):
    def __init__(self, since_date: date = date.today()-timedelta(days=1)) -> None:
        super.__init__(since_date)
        self.subject = f"Daily Newsletter: {date.today().strftime('%A, %B %-d %Y')}"

    def _gather_data(self) -> dict:
        # pulling data from dynamodb
        pass

    def _synthesize(self, data: dict) -> dict:
        synthesizer = EmailSynthesizer()
        categorized = synthesizer.categorize(data)
        synthesized = synthesizer.synthesize(categorized)
        return synthesized

    def _send(self, data: dict):
        self._send_email(
            sender=os.environ["MY_EMAIL_ADDRESS"],
            recipient=os.environ["MY_EMAIL_ADDRESS"],
            subject=self.subject,
            body_html=self._to_html(data),
            aws_region=os.environ["AWS_DEFAULT_REGION"]
        )

    def _to_html(self, data: dict):
        html = f"""
        <html>
        <head></head>
        <body>
        <h1>Good Morning! Todays News:</h1>
        """
        for key in data.keys():
            html += f"<h2>{key.value}</h2>\n"
            html += f"<p>{data[key]}</p>\n"
        html += """
        <div></div>
        <p>Have a good day!</p>
        </body>
        </html>
        """

    def _send_email(self, sender, recipient, subject, body_html, aws_region):
        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=aws_region)

        # Try to send the email.
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': body_html,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
