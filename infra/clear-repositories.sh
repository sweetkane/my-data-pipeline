#!/bin/bash

repository_names=$(
    aws ecr describe-repositories \
        --query 'repositories[*].repositoryName' \
        --output text
)

for repository_name in $repository_names; do

    image_digests=$(
        aws ecr list-images \
            --repository-name $repository_name \
            --query 'imageIds[*].imageDigest' \
            --output text
    )

    for digest in $image_digests; do
        aws ecr batch-delete-image \
            --repository-name $repository_name \
            --image-ids imageDigest=$digest
    done

    aws ecr delete-repository --repository-name $repository_name
done
