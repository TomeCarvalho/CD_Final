#!/bin/bash

docker pull docker.io/diogogomes/cd2021
docker stop server
docker rm server
docker run -ti --env PASSWORD_SIZE=2 --name server diogogomes/cd2021

