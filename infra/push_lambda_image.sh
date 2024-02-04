#!/bin/bash

#######################################################################
#################### ASSERT ENV VARIABLES SET #########################

if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "Err: AWS_ACCOUNT_ID environment variable is not set"
    exit 1
fi
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "Err: AWS_ACCESS_KEY_ID environment variable is not set"
    exit 1
fi
if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "Err: AWS_SECRET_ACCESS_KEY environment variable is not set"
    exit 1
fi
if [ -z "$AWS_DEFAULT_REGION" ]; then
    echo "Err: AWS_DEFAULT_REGION environment variable is not set"
    exit 1
fi
if [ -z "$MY_EMAIL_ADDRESS" ]; then
    echo "Err: MY_EMAIL_ADDRESS environment variable is not set"
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
#######################################################################
########################## HANDLE ARGS ################################

if [ $# -eq 0 ]; then
    echo "Usage:    $0 <lambda_name> <repo_name>(optional)"
    exit 1
fi
lambda_name=$1

repo_name=repo_$lambda_name
if [ $# -eq 2 ]; then
    repo_name=$2
fi

#######################################################################
lambda_tag=latest
repo_tag=$(uuidgen)

# create image
docker build \
    --file infra/Dockerfile \
    --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --build-arg AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    --build-arg MY_EMAIL_ADDRESS=$MY_EMAIL_ADDRESS \
    --build-arg OPENAI_API_KEY=$OPENAI_API_KEY \
    --build-arg NEWS_API_KEY=$NEWS_API_KEY \
    --build-arg RAPID_API_KEY=$RAPID_API_KEY \
    --platform linux/amd64 \
    -t $lambda_name:$lambda_tag . \
    >/dev/null

# point docker at ECR
aws ecr get-login-password \
    --region $AWS_DEFAULT_REGION | \
    docker login \
        --username AWS \
        --password-stdin \
        $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com \
        >/dev/null

#create repo
repo_uri=$(aws ecr create-repository \
    --repository-name "$repo_name" \
    --region "$AWS_DEFAULT_REGION" \
    --image-scanning-configuration scanOnPush=true \
    --image-tag-mutability MUTABLE \
    --query repository.repositoryUri \
    --output text \
    2>/dev/null \
)
if [[ $? -ne 0 ]]; then
    repo_uri=$(aws ecr describe-repositories \
        --repository-names $repo_name \
        --query repositories[0].repositoryUri \
        --output text \
    )
fi

# tag local image into ECR repo
docker tag $lambda_name:$lambda_tag $repo_uri:$repo_tag >/dev/null

# push local to ECR
docker push $repo_uri:$repo_tag >/dev/null

# return the image uri
echo "$repo_uri:$repo_tag"
