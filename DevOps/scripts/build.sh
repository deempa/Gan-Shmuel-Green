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
    if [[ $? -eq 0 ]]; then
        echo "Clone ${repo_name} repo was Successful."
    else
        echo "Clone ${repo_name} was Failed."
        exit 1
    fi
}

build() (
    local app_name=$1
    echo "Start Building"

    if [[ $app_name == "billing" ]]; then
        echo "Building Billing Image"
        cd "$repo_name/Billing/"
        docker build --quiet --no-cache -t billing_image .
        if [[ $? -eq 0 ]]; then
            echo "Build Billing image was Successful."
        else
            echo "Build Billing image was Failed."
            exit 1
        fi

    elif [[ $app_name == "weight" ]]; then
        echo "Building Weight Image"
        cd "$repo_name/Weight/app/"
        docker build --quiet --no-cache -t weight_image .  
        if [[ $? -eq 0 ]]; then
            echo "Build Weight image was Successful."
        else
            echo "Build Weight image was Failed."
            exit 1
        fi  
    fi
)

cleaning()
{
    docker rmi -f billing_image &> /dev/null
    docker rmi -f weight_image &> /dev/null
}

compose_to_test()
{
    echo "Delpoying to test"
    docker-compose --project-name test --env-file ./config/.env.test up -d
        if [[ $? -eq 0 ]]; then
        echo "Deploy Test env was Successful."
    else
        echo "Deploy Test env was Failed."
        exit 1
    fi
}

run_e2e_test()
(
    echo "Running E2E tests...."
    echo "Billing Testing"
    cd "${repo_name}/Billing/"
    pytest test.py
    echo $?
    exit 1
    echo "Billing Tests success"
)

terminate_test(){
    docker-compose --project-name test down --rmi local --remove-orphans
}

compose_to_production()
{
    echo "Delpoying to production"
    docker-compose --project-name production --env-file ./config/.env.prod up -d
    if [[ $? -eq 0 ]]; then
        echo "Deploy Production env was Successful."
    else
        echo "Deploy Production env was Failed."
        exit 1
    fi
}

repo_name=$1
repo_url=$2

clone $repo_name $repo_url
if [[ $? -eq 1 ]]; then
    exit 1
fi

cleaning

build billing
if [[ $? -eq 1 ]]; then
    exit 1
fi

build weight
if [[ $? -eq 1 ]]; then
    exit 1
fi

compose_to_test
if [[ $? -eq 1 ]]; then
    exit 1
fi

run_e2e_test
if [[ $? -eq 1 ]]; then
    exit 1
fi

terminate_test

compose_to_production
if [[ $? -eq 1 ]]; then
    exit 1
fi
