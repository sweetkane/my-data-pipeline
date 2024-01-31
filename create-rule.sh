#!/bin/bash

aws events put-rule \
    --name "daily_lambda_trigger" \
    --schedule-expression "cron(0 8 * * ? *)"

aws lambda add-permission \
  --function-name "YourLambdaFunctionName" \
  --statement-id "EventBridgeRule" \
  --action "lambda:InvokeFunction" \
  --principal "events.amazonaws.com" \
  --source-arn arn:aws:events:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:rule/rule-name

aws events put-targets \
    --rule "daily_lambda_trigger" \
    --targets "Id"="1","Arn"="arn:aws:lambda:$AWS_DEFAULT_REGION:$AWS_ACCOUNT_ID:function:$lambdaname"
