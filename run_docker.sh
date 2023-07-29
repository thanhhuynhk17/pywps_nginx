#!/bin/bash

echo "killing old docker processes"
docker-compose rm -sf

echo "building docker containers"
docker-compose up --build -d