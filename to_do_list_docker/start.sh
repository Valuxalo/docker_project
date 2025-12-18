#!/bin/bash

docker stop to_do_list

docker build -t to_do_list .

docker run --rm -d --network=host --name to_do_list to_do_list
