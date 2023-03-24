#!/bin/bash

clone_repo ()
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

clean_images()
{
    echo "Cleaning up Docker images..."
    docker rmi -f billing_image weight_image &> /dev/null || true
}

deploy_to_test()
{
    echo "Deploying to test environment..."
    docker-compose --project-name test --env-file ./config/.env.test up -d
        if [[ $? -eq 0 ]]; then
        echo "Deployment to test environment was successful."
    else
        echo "Deployment to test environment was failed."
        exit 1
    fi
}

run_e2e_test()
(
    sleep 5
    echo "Running E2E tests...."
    echo "Billing Testing"
    cd "${repo_name}/Billing/tests"
    pytest --quiet test.py
    if [[ $? -eq 0 ]]; then
        echo "Billing Tests success"
    else
        echo "Billing Tests Failed"
        exit 1
    fi

    echo "Weight Testing"
    cd "../../Weight/app/tests"
    pytest --quiet test.py
    if [[ $? -eq 0 ]]; then
        echo "Weight Tests success"
    else
        echo "Weight Tests Failed"
        exit 1
    fi
)

cleanup_test_env(){
    echo "Cleaning up test environment..."
    docker-compose --project-name test --env-file ./config/.env.test down --rmi local --remove-orphans -v
    echo "Cleanup of test environment was successful."
}

deploy_to_production()
{
    echo "Delpoying to production"
    docker-compose --project-name production --env-file ./config/.env.prod up -d
    if [[ $? -eq 0 ]]; then
        echo "Deployment to production environment was successful."
    else
        echo "Deployment to production environment was failed."
        exit 1
    fi
}

# Main Script

repo_name="$1"
repo_url="$2"

clone_repo "${repo_name}" "${repo_url}"
if [[ $? -eq 1 ]]; then
    exit 1
fi

clean_images

build billing || exit $?

build weight || exit $?

deploy_to_test || exit $?

run_e2e_test || exit $?

cleanup_test_env || exit $?

deploy_to_production || exit $?


