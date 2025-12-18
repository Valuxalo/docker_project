#!/bin/bash

docker stop short_url

docker build -t short_url .

docker run --rm -d --network=host --name short_url short_url
