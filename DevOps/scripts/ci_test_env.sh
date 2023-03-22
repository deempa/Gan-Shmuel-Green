#!/bin/bash

clone()(
    local repo_url=$1
    local branch_name=$2
    git clone --branch ${branch_name} ${repo_url}
)

build()(
    local branch_name=$1
    if [[ ${branch_name} == "Billing" ]]; then
        cd "$repo_name/Billing/"
        docker build --no-cache -t billing_image .
    elif [[ ${branch_name} == "Weight" ]]; then
        docker build --no-cache -t weight_image --file "$repo_name/Weight/app/Dockerfile"
    elif [[ ${branch_name} == "main" ]]; then
        docker build --no-cache -t billing_image --file "$repo_name/Billing/Dockerfile"
        docker build --no-cache -t weight_image --file "$repo_name/Weight/app/Dockerfile"
)

repo_name=$1
repo_url=$2
branch_name=$3

clone ${repo_url} ${branch_name}

build ${branch_name}