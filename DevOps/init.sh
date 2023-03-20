#!/bin/bash

docker build -t devops_app_image --no-cache .

docker run -d --name devops_app devops_app_image