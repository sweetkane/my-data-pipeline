#!/bin/bash

########################## HANDLE ARGS ################################

if [ $# -eq 0 ]; then
    echo "Usage:    $0 <lambda_name>"
    exit 1
fi
lambda_name=$1

stack_name=stack--$lambda_name

#######################################################################

# push sender lambda image
echo "push sender lambda image: STARTING"
image_uri=$(./infra/sender_push_lambda.sh "robonews_sender")
if [[ $? -ne 0 ]]; then
    echo "push sender lambda image: FAILED"
    exit 1
fi

echo "push sender lambda image: DONE"

# push subscribe/unsubscribe lambda code to S3

# push subscribe.html, unsubcribe.html to S3




echo "cloudformation deploy: STARTING"

aws cloudformation deploy \
    --template-file infra/stack.yml \
    --stack-name $stack_name \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    LambdaFunctionName=$lambda_name \
    ImageUri=$image_uri

echo "cloudformation deploy: DONE"
