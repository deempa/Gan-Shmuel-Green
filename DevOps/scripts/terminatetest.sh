#!/bin/bash

docker-compose --project-name test --env-file ./config/.env.test down --rmi local --remove-orphans -v
