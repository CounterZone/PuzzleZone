#!/bin/bash
WORKER_NUMBER=1

docker-compose -f docker-compose-test.yml build
docker-compose -f docker-compose-test.yml  up 
