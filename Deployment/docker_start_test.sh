#!/bin/bash
WORKER_NUMBER=2

docker-compose -f docker-compose-test.yml build
docker-compose -f docker-compose-test.yml  up --scale worker=2
