#!/bin/bash

image_name="middle-platfrom"
port=8888
project_path="$(pwd)"

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not available"
    exit 1
fi

if ! docker images -q $image_name &> /dev/null; then
    echo "Image '$image_name' does not exist"
    exit 1
fi

docker run -it -p $port:$port -v $project_path:/app $image_name
