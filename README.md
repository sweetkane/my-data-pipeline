# 🤖RoboNews🤖
RoboNews is a cloud-hosted LLM-powered bot that delivers a summary of the latest news to your email inbox each morning.

## Usage

### Sign Up For Mailing List
TODO

### Create your own
To create your own RoboNews bot with this repo, you can
1. clone the repo
2. add the needed environment variables (found at the top of `infra/push_lambda_image.sh`)
3. run `./infra/deploy.sh`

## Technical details
- infra
  - aws: ecs, lambda, cloudformation, eventbridge
  - docker
- src
  - python
  - langchain
  - plugin architecture

- kanesweet s3 bucket is not managed by cloudformation
