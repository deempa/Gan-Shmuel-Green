#!/bin/bash

docker build -t devops_app_image --no-cache .

docker run -d -v /var/run/docker.sock:/var/run/docker.sock --name devops_app -p 8081:8081 devops_app_image