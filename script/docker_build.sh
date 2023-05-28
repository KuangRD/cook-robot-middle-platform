#!/bin/bash

image_name="middle-platfrom"

# Set the Dockerfile path
dockerfile_path="$(pwd)/Dockerfile"

# Check if Docker is installed and available
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not available"
    exit 1
fi

# Check if the Dockerfile exists
if [ -f "$dockerfile_path" ]; then
    # Build the Docker image
    docker buildx build -t $image_name -f "$dockerfile_path" $(pwd)
else
    echo "Dockerfile not found "
    exit 1
fi