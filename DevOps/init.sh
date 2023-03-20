#!/bin/bash

docker build -t devops_app_image --no-cache .

docker run -d --privileged --name devops_app -p 8081:8081 devops_app_image