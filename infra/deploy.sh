#!/bin/bash

########################## HANDLE ARGS ################################

if [ $# -eq 0 ]; then
    echo "Usage:    $0 <lambda_name>"
    exit 1
fi
lambda_name=$1

stack_name=stack--$lambda_name

#######################################################################

# push lambda image
echo "push lambda image: STARTING"
image_uri=$(./infra/push_lambda_image.sh $lambda_name)
if [[ $? -ne 0 ]]; then
    echo "push lambda image: FAILED"
    exit 1
fi

echo "push lambda image: DONE"
echo "cloudformation deploy: STARTING"

aws cloudformation deploy \
    --template-file infra/stack_template.yaml \
    --stack-name $stack_name \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
    LambdaFunctionName=$lambda_name \
    ImageUri=$image_uri

echo "cloudformation deploy: DONE"
