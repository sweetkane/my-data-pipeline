# 🤖RoboNews🤖
RoboNews is a cloud native email newsletter that delivers weekly news about AI and LLMs, written by an LLM!

[Subscribe](https://kanesweet.com/robonews/subscribe)

## Technical details
- Uses a LOT of AWS services
  - Cloudformation, Lambda, S3, DynamoDB, EventBridge, KMS, SES, ECS, Route 53, Cloudfront
- Subscription page uses S3 to serve static web content, delivered through Cloudfront CDN which holds SSL cert
- Unsubscribe button at the bottom of emails uses signed URLs so users can only unsubscribe their own account
  - URLs are encrypted/decrypted with KMS
- Newsletter is sent by a lambda function which
  - Is defined in an ECS container (If I were to do it again I would use S3 and lambda layers)
  - Is triggered by an EventBridge cron job
  - Gets headlines from RSS feeds, and then summarizes them with Langchain-OpenAI
