#!/bin/bash

docker build --quiet -t devops_app_image --no-cache .

docker rm -f devops_app

docker run -it -v /var/run/docker.sock:/var/run/docker.sock --name devops_app -p 8081:8081 devops_app_image