#!/bin/bash

docker build -t devops_app_image --no-cache .

docker run -d --name devops_app -p 8081:8081 -v /var/run/docker.sock:/var/run/docker.sock devops_app_image