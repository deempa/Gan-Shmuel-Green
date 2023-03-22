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
    git clone --quiet $repo_url
    echo "Cloning Finished"
}

build() (
    local app_name=$1
    echo "Start Building"

    if [[ $app_name == "billing" ]]; then
        echo "Building Billing Image"
        cd "$repo_name/Billing/"
        docker build --quiet --no-cache -t billing_image .

    elif [[ $app_name == "weight" ]]; then
        echo "Building Weight Image"
        cd "$repo_name/Weight/app/"
        docker build --quiet --no-cache -t weight_image .    
    fi
)

cleaning()
{
    docker rmi -f billing_image &> /dev/null
    docker rmi -f weight_image &> /dev/null
}

compose_to_production()
{
    echo "Delpoying to production"
    docker-compose --project-name production --env-file ./config/.env up -d
}

repo_name=$1
repo_url=$2

clone $repo_name $repo_url

cleaning

build billing
build weight

compose_to_production
