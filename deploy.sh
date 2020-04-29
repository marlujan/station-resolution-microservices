#!/usr/bin/env bash

IMAGE_NAME='station-resolution-ms'

case $1 in
  build)
    echo "Removing old containers and images"
    docker rm -f "${IMAGE_NAME}"
    docker image rm "${IMAGE_NAME}":latest
    echo "Building..."
    docker build -f Dockerfile -t "${IMAGE_NAME}":latest .
    echo "Successfully built image"
    ;;
  run)
    echo "Starting..."
    docker rm -f "${IMAGE_NAME}"
    docker run -d -p 5000:5000 --name "${IMAGE_NAME}" "${IMAGE_NAME}":latest
    echo "Successfully started container"
    ;;
  stop)
    echo "Stopping..."
    docker stop "${IMAGE_NAME}"
    docker rm -f "${IMAGE_NAME}"
    echo "Successfully stopped container"
    ;;
  *)
		echo "[ERROR] Invalid Option"
    ;;
esac
