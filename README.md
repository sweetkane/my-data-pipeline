# my-twitter-bot

#### logic
producers: \[lambda]
- get data from datasource
- write it to dynamodb

database: dynamodb
- db\[datatype: (headline,)][date: date] = todays_headlines

consumers: \[lambda]
- get data
- pass it to langchain model
- send output to twitter api


I might be able to use cloudformation as part of a pipeline that comes after my scripted lambda deployment.
Potentially I just script the part where I deploy the container to ECR, then after that I create the stack

deployment-pipeline.sh
``` bash
cd producer
./deploy-lambda.sh producer-lambda
cd ../consumer
./deploy-lambda.sh consumer-lambda
cd ..
aws cloudformation create-stack \
    --stack-name twitterbot
    --template-body file://stack-template.yaml
```


./deploy-lambda.sh my-data-pipeline
aws lambda invoke \
    --function-name my-data-pipeline \
    --payload '{"datasources": ["connexun_news", "news_now"], "clients": ["email"]}'

aws lambda invoke \
    --function-name my-data-pipeline \
    --cli-binary-format raw-in-base64-out \
    --payload '{"datasources":["news_now"],"transforms":["news_synthesizer"],"clients": ["email"]}' \
    res.txt


'{"datasources":["news_now"],"transforms":["news_synthesizer"],"clients": ["email"]}'

https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions
https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html#examples

repo regex:
(?:[a-z0-9]+(?:[._-][a-z0-9]+)*/)*[a-z0-9]+(?:[._-][a-z0-9]+)*

stack regex:
[a-zA-Z][-a-zA-Z0-9]*|arn:[-a-zA-Z0-9:/._+]*

TODO
- migrate from event bridge rule to scheduler PRIORITY=LOW
