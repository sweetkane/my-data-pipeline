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
exit 0

# create function
echo "$0: creating function named $lambda_name"
aws lambda delete-function --function-name "$lambda_name" 2>/dev/null
function_arn=$(aws lambda create-function \
    --function-name "$lambda_name" \
    --package-type Image \
    --code ImageUri=$image_uri \
    --role arn:aws:iam::$AWS_ACCOUNT_ID:role/$role \
    --timeout 300 \
    --query FunctionArn \
    --output text \
)

# create events rule
lambda_payload="'{\"datasources\":[\"connexun_news\",\"news_now\"],\"clients\":[\"email\"]}'"

echo "$0: creating events rule daily_lambda_trigger"
aws events delete-rule \
    --name "daily_lambda_trigger" \
    2>/dev/null
rule_arn=$(aws events put-rule \
    --name "daily_lambda_trigger" \
    --schedule-expression "cron(0 8 * * ? *)" \
    --query RuleArn \
    --output text \
)

# apply events rule
echo "$0: applying daily_lambda_trigger to lambda"
aws lambda add-permission \
    --function-name "$lambda_name" \
    --statement-id "EventBridgeRule" \
    --action "lambda:InvokeFunction" \
    --principal "events.amazonaws.com" \
    --source-arn $rule_arn \
    >/dev/null
aws events put-targets \
    --rule "daily_lambda_trigger" \
    --targets "Id"="1","Arn"="$function_arn","Input"=$lambda_payload \
    >/dev/null

echo "$0: DONE"
