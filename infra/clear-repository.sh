#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage:    $0 <repo_name>"
    exit 1
fi
repository_name=$1

image_digests=$(aws ecr list-images --repository-name $repository_name --query 'imageIds[*].imageDigest' --output text)

for digest in $image_digests; do
    aws ecr batch-delete-image --repository-name $repository_name --image-ids imageDigest=$digest
done
