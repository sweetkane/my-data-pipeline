# 🤖RoboNews🤖
RoboNews is a cloud native email newsletter that delivers weekly news about AI and LLMs, written by an LLM!

[Subscribe](https://kanesweet.com/robonews/subscribe)

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
- use cors to block traffic from outside s3?
