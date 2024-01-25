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


curl https://en.wikipedia.org/wiki/Portal:Current_events > temp.html
