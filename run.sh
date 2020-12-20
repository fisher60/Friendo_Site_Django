#!/bin/bash

if pgrep "docker" >/dev/null; then
	echo "Docker is running..."
else
	echo "Docker is not running"
	echo "enabling docker..."
	systemctl enable docker
	systemctl start docker
	echo "Docker is enabled"
fi

echo "Running docker compose..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up 2>error.log

if [ $? -eq 1 ]; then
	echo "Error occurred while running docker-compose. Please check the error file for futher info."
else
	echo "Container succesffuly running."
fi
