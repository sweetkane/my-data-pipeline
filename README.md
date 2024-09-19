# 🤖RoboNews🤖 [![Button Shield]][Shield]
RoboNews is a serverless email newsletter that delivers weekly news about AI and LLMs, written by an LLM!

## Technical details
- Uses a LOT of AWS services
  - Cloudformation, Lambda, S3, DynamoDB, EventBridge, KMS, SES, ECS, Route 53, Cloudfront
- Serverless website design
  - Subscription page uses S3, Cloudfront with SSL, and Route 53 to create a serverless website with HTTPS
- Signed URLs
  - Unsubscribe button uses signed URLs so users can only unsubscribe their own account
  - URLs are encrypted/decrypted with KMS
- Containerized Lambda
  - Newsletter is sent by a lambda function which
    - Is defined in an ECS container which handles dependencies
      - (If I were to do it again I would use S3 and lambda layers tbh)
    - Is triggered by an EventBridge cron job
    - Gets headlines from RSS feeds, and then summarizes them with Langchain-OpenAI

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.


<!---------------------------------[ Badges ]---------------------------------->

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[Button Shield]: https://img.shields.io/badge/Click%20to%20Subscribe!-37a779?style=for-the-badge
[Shield]: https://kanesweet.com/robonews/subscribe
