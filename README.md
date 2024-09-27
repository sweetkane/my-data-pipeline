# 🤖RoboNews🤖 [![Button Shield]][Shield]
RoboNews is a serverless email newsletter that delivers weekly news about AI and LLMs, written by an LLM!

## Technical details
- Uses a LOT of AWS services
  - Cloudformation, Lambda, S3, DynamoDB, EventBridge, KMS, ECS, Route 53, Cloudfront
- Serverless design
  - Subscription page uses S3, Cloudfront, Certificate Manager, and Route 53 to create a serverless website with HTTPS
- One-Click Deployment
  - The project includes a deployment script which uses the AWS CLI to push source code to ECS and S3, and then deploys the Cloudformation template
  - If I were to do it again I'd probably use CDK instead of the CLI
  - A future addition that I decided was out of scope for now is a CI/CD pipeline that automatically deploys changes when they're pushed to origin
- Signed URLs
  - Confirm-Email & Unsubscribe buttons use signed URLs so users can only manage their own account
  - URLs are encrypted/decrypted with KMS
- Containerized Lambda
  - Newsletter is sent by a lambda function in an ECS container
    - If I were to do it again I would use S3 and lambda layers tbh
  - Lambda is triggered by an EventBridge cron job
  - Source code uses a "plugin" architecture making it easy to add news sources and output types
  - Gets headlines from RSS feeds, and then summarizes them with Langchain-OpenAI


## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.


<!---------------------------------[ Badges ]---------------------------------->

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[Button Shield]: https://img.shields.io/badge/Click%20to%20Subscribe!-37a779?style=for-the-badge
[Shield]: https://kanesweet.com/robonews/subscribe
