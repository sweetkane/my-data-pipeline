from datetime import date, timedelta
import boto3
from botocore.exceptions import ClientError
import os

class EmailClient(IClient):
    def __init__(self, since_date: date = date.today()-timedelta(days=1)) -> None:
        super.__init__(since_date)
        self.subject = f"Daily Newsletter: {date.today().strftime('%A, %B %-d %Y')}"

    def _gather_data(self) -> dict:
        # pulling data from dynamodb
        pass

    def _synthesize(self, data: dict) -> dict:
        pass

    def _send(self, payload: dict):
        self._send_email(
            sender=os.environ["MY_EMAIL_ADDRESS"],
            recipient=os.environ["MY_EMAIL_ADDRESS"],
            subject=self.subject,
            body_html=self._to_html(payload),
            aws_region=os.environ["AWS_DEFAULT_REGION"]
        )

    def _to_html(self, payload):
        return f"""
        <html>
        <head></head>
        <body>
        <h1>Good Morning! Todays News:</h1>
        <h2>World</h2>
        <p>{payload["world"]}</p>
        <h2>National Politics</h2>
        <p>{payload["national"]}</p>
        <h2>Entertainment</h2>
        <p>{payload["entertainment"]}</p>
        <h2>Science</h2>
        <p>{payload["science"]}</p>
        <h2>Sports</h2>
        <p>{payload["sports"]}</p>
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
