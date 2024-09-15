#!/bin/bash

# Variables
bucket_name=kanesweet
stack_name=RobonewsRootStack

## Sender
sender_lambda_name="sender_lambda"
sender_template_url="$bucket_name/robonews/sender/stack.yml"

## Subscription
subscription_s3_path="$bucket_name/robonews/subscription"
subscription_template_url="$subscription_s3_path/stack.yml"
subscribe_lambda_name="subscribe_lambda"
unsubscribe_lambda_name="unsubscribe_lambda"

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

# upload sender template to S3
echo "[deploy.sh] upload sender template to S3: STARTING"
aws s3 cp sender/stack.yml "s3://$sender_template_url"
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] upload sender template to S3: FAILED"
    exit $?
fi
echo "[deploy.sh] upload sender template to S3: SUCCEEDED"


### Subscription ###

# upload lambda zips to S3
echo "[deploy.sh] upload subscription lambdas to S3: STARTING"
tmp=$(./subscription/push_lambda.sh $subscribe_lambda_name "s3://$subscription_s3_path")
tmp=$(./subscription/push_lambda.sh $unsubscribe_lambda_name "s3://$subscription_s3_path")
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] upload subscription lambdas to S3: FAILED"
    exit $?
fi
echo "[deploy.sh] upload subscription lambdas to S3: SUCCEEDED"

# upload html to S3
echo "[deploy.sh] upload html to S3: STARTING"
aws s3 cp subscription/subscribe.html "s3://$subscription_s3_path/subscribe.html"
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] upload html to S3: FAILED"
    exit $?
fi
echo "[deploy.sh] upload html to S3: SUCCEEDED"

# upload subscription template to S3
echo "[deploy.sh] upload subscription template to S3: STARTING"
aws s3 cp subscription/stack.yml "s3://$subscription_template_url"
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] upload subscription template to S3: FAILED"
    exit $?
fi
echo "[deploy.sh] upload subscription template to S3: SUCCEEDED"

# deploy stack
echo "[deploy.sh] deploy stack: STARTING"
aws cloudformation deploy \
    --template-file stack.yml \
    --stack-name $stack_name \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    BucketName="$bucket_name" \
    SenderLambdaName="$sender_lambda_name" \
    SenderLambdaImageUri="$sender_lambda_image_uri" \
    SenderTemplateUrl="$sender_template_url" \
    SubscribeLambdaName="$subscribe_lambda_name" \
    UnsubscribeLambdaName="$unsubscribe_lambda_name" \
    SubscriptionTemplateUrl="$subscription_template_url"
if [[ $? -ne 0 ]]; then
    echo "[deploy.sh] deploy stack: FAILED"
    exit $?
fi
echo "[deploy.sh] deplay stack: SUCCEEDED"
