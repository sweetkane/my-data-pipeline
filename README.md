# 🤖RoboNews🤖
RoboNews is a serverless email newsletter that delivers weekly news about AI and LLMs, written by an LLM!

[Subscribe](https://kanesweet.com/robonews/subscribe)

## Technical details
- Uses a LOT of AWS services
  - Cloudformation, Lambda, S3, DynamoDB, EventBridge, KMS, SES, ECS, Route 53, Cloudfront
- Serverless website design
  - Subscription page uses S3, Cloudfront with SSL, and Route 53 to create a serverless website accessible with HTTPS
- Signed URLs
  - Unsubscribe button at the bottom of emails uses signed URLs so users can only unsubscribe their own account
  - URLs are encrypted/decrypted with KMS
- Containerized Lambda
  - Newsletter is sent by a lambda function which
    - Is defined in an ECS container which handles dependencies (If I were to do it again I would use S3 and lambda layers tbh)
    - Is triggered by an EventBridge cron job
    - Gets headlines from RSS feeds, and then summarizes them with Langchain-OpenAI
