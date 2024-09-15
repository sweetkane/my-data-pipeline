#!/bin/bash

### ASSERTS ###

if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "Err: AWS_ACCOUNT_ID environment variable is not set"
    exit 1
fi
if [ -z "$AWS_DEFAULT_REGION" ]; then
    echo "Err: AWS_DEFAULT_REGION environment variable is not set"
    exit 1
fi
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Err: OPENAI_API_KEY environment variable is not set"
    exit 1
fi
if [ -z "$NEWS_API_KEY" ]; then
    echo "Err: NEWS_API_KEY environment variable is not set"
    exit 1
fi
if [ -z "$RAPID_API_KEY" ]; then
    echo "Err: RAPID_API_KEY environment variable is not set"
    exit 1
fi

docker -v >/dev/null
if [[ $? -ne 0 ]]; then
    echo "Err: docker not installed"
    exit 1
fi

### VARIABLES ###

if [ $# -ne 2 ]; then
    echo "Usage:    $0 <lambda_name> <tag>"
    exit 1
fi
lambda_name=$1

repo_name="${lambda_name}_repo"

lambda_tag=latest
repo_tag=$2

### SCRIPT BODY ###

# create image
docker build \
    --file sender/Dockerfile \
    --build-arg OPENAI_API_KEY=$OPENAI_API_KEY \
    --build-arg NEWS_API_KEY=$NEWS_API_KEY \
    --build-arg RAPID_API_KEY=$RAPID_API_KEY \
    --platform linux/amd64 \
    -t $lambda_name:$lambda_tag . \
    >/dev/null

# point docker at ECR
aws ecr get-login-password \
    --region $AWS_DEFAULT_REGION |
    docker login \
        --username AWS \
        --password-stdin \
        $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com \
    >/dev/null

#create repo
repo_uri=$(
    aws ecr create-repository \
        --repository-name "$repo_name" \
        --region "$AWS_DEFAULT_REGION" \
        --image-scanning-configuration scanOnPush=true \
        --image-tag-mutability MUTABLE \
        --query repository.repositoryUri \
        --output text \
        2>/dev/null
)
if [[ $? -ne 0 ]]; then
    repo_uri=$(
        aws ecr describe-repositories \
            --repository-names $repo_name \
            --query repositories[0].repositoryUri \
            --output text
    )
fi

# tag local image into ECR repo
docker tag $lambda_name:$lambda_tag $repo_uri:$repo_tag >/dev/null

# push local to ECR
docker push $repo_uri:$repo_tag >/dev/null

# return the image uri
echo "$repo_uri:$repo_tag"
