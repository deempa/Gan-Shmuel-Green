#!/bin/bash

clone ()
{
    local repo_name=$1
    local repo_url=$2
    echo $repo_name
    echo $repo_url
    if [ -d $repo_name ]; then
        echo "Folder 'repo' exists. Deleting..."
        rm -rf $repo_name
    fi
    git clone $repo_url
    echo "Cloning Finished"
}

build (
    local app_name=$1
    docker rmi -f billing_image &> /dev/null
    docker rmi -f weight_image &> /dev/null
    echo "Building..."

    if [[ $app_name == "billing" ]]; then
        cd "$repo_name/Billing/"
        docker build --no-cache -t billing_image .
        echo "Build Billing"
    elif [[ $app_name == "weight" ]]; then
        cd "$repo_name/Weight/app/"
        docker build --no-cache -t weight_image .
        echo "Build Weight"
    fi
)

repo_name=$1
repo_url=$2

clone $repo_name $repo_url

build billing
build weight