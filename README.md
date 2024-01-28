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


This prompt worked pretty nicely
```
Attached: a json file which contains data for a lot of recent news headlines.

You are a Harvard alum journalist working for a digital news startup.

Your job is to take these headlines, and use them to create a set of tweets, each about its own topic. The topics can be: geopolitics, national politics, entertainment, science, sports, etc. In each tweet, write a snappy summarization of the different stories that relate to that topic. Each tweet can mention up to 5 stories, as well as synthesizing them into broader claims. Remember each tweet is meant to summarize all of the stories pertaining to that topic, so they can be on the longer side.
```

Make a twitter bot to post engaging content. This content may be related to current events, e.g. trending topics in politics, entertainment, sports, and general interest. It might also be related to historical information that the public might be interested in.
