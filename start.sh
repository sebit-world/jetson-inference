#!/bin/bash

export ARCH="aarch64"
image_name="jetson-inference:latest"

if [[ "$(docker images -q ${image_name} 2> /dev/null)" == "" ]];
then
    docker build -t ${image_name} -f Dockerfile.custom .
fi

./docker/run.sh -c ${image_name}
