#!/bin/bash

# Variables
bucket_name=robonews

## Sender
sender_lambda_name="sender_lambda"
sender_template_url="s3://kanesweet/$bucket_name/sender/stack.yml"

## Subscription
subscription_template_url="s3://kanesweet/$bucket_name/subscription/stack.yml"

stack_name=stack--$lambda_name

#######################################################################

### Sender ###

# push sender lambda image to ECR
echo "[deploy.sh] push sender lambda image: STARTING"
sender_lambda_image_uri=$(./sender/push_lambda.sh $sender_lambda_name)
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] push sender lambda image: FAILED"
    exit $?
fi
echo "[deploy.sh] push sender lambda image: SUCCEEDED"

# upload sender stack to S3
echo "[deploy.sh] upload sender stack to S3: STARTING"
aws s3 cp sender/stack.yml $sender_template_url
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] upload sender stack to S3: FAILED"
    exit $?
fi
echo "[deploy.sh] upload sender stack to S3: SUCCEEDED"


### Subscription ###

# upload sender stack to S3
echo "[deploy.sh] upload subscription stack to S3: STARTING"
aws s3 cp subscription/stack.yml $subscription_template_url
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] upload subscription stack to S3: FAILED"
    exit $?
fi
echo "[deploy.sh] upload subscription stack to S3: SUCCEEDED"

### Final ###
exit 1

# deploy stack
echo "[deploy.sh] deploy stack: STARTING"
aws cloudformation deploy \
    --template-file stack.yml \
    --stack-name $stack_name \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    SenderLambdaName=$sender_lambda_name \
    SenderLambdaImageUri=$sender_lambda_image_uri \
    SenderTemplateUrl=$sender_template_url
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] deploy stack: FAILED"
    exit $?
fi
echo "[deploy.sh] deplay stack: SUCCEEDED"

# push subscribe/unsubscribe lambda code to S3

# push subscribe.html, unsubcribe.html to S3




echo "cloudformation deploy: STARTING"



echo "cloudformation deploy: DONE"
