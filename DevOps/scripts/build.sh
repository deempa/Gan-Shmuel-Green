#!/bin/bash

clone ()
{
    local repo_name=$1
    local repo_url=$2
    if [ -d $repo_name ]; then
        echo "Folder 'repo' exists. Deleting..."
        rm -rf $repo_name
    fi
    git clone $repo_url
    echo "Cloning Finished"
    build
}

build ()
{
    echo "Building..."
}

clone $1 $2
