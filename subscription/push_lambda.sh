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

### VARIABLES ###

if [ $# -ne 3 ]; then
    echo "Usage:    $0 <lambda_name> <s3_path> <tag>"
    exit 1
fi
lambda_name=$1
s3_path=$2
tag=$3

lambda_tag=latest
repo_tag=$(uuidgen)

### SCRIPT BODY ###

zip tmp.zip subscription/$lambda_name.py
aws s3 cp tmp.zip $s3_path/$lambda_name-$tag.zip
rm tmp.zip
