# 🤖RoboNews🤖
RoboNews is a cloud native email newsletter that delivers weekly news about AI and LLMs, written by an LLM!

[![Sponsor on GitHub](https://gist.github.com/cxmeel/0dbc95191f239b631c3874f4ccf114e2/raw/github_sponsor-compact.svg)](https://github.com/sponsors/cxmeel) [![View Itch.io Store](https://gist.github.com/cxmeel/0dbc95191f239b631c3874f4ccf114e2/raw/itch-compact.svg)](https://cxmeel.itch.io)

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
