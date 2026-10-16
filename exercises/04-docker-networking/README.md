# Exercise 4: Docker Networking

## Objective
Create a custom Docker bridge network and connect Flask, MySQL, and Redis containers.

## Technologies
- Docker
- Docker bridge networking
- Flask
- MySQL 8
- Redis 7

## Files
- app.py: Flask REST API with an /about endpoint.
- requirements.txt: Python dependencies.
- Dockerfile: Flask container configuration.
- README.md: Setup, testing, and cleanup instructions.

## Network Setup
Create the custom bridge network:

    docker network create --driver bridge my-bridge-net

Inspect it:

    docker network inspect my-bridge-net

## Build the Flask Image

    docker build -t simple-flask-api:1.0 .

## Start the Containers

    docker run -d --name ex4-mysql --network my-bridge-net -e MYSQL_ROOT_PASSWORD=DevOpsLabTemp123 -e MYSQL_DATABASE=labdb mysql:8.0

    docker run -d --name ex4-redis --network my-bridge-net redis:7-alpine

    docker run -d --name ex4-flask --network my-bridge-net -p 5001:5001 simple-flask-api:1.0

The MySQL password above is a disposable lab credential. Do not reuse it.

## Verify

Check running containers:

    docker ps --filter "name=ex4-"

Test the REST API:

    Invoke-RestMethod http://localhost:5001/about

Test container-name resolution and connectivity:

    docker exec ex4-flask ping -c 3 ex4-mysql

    docker exec ex4-flask ping -c 3 ex4-redis

Inspect network members:

    docker network inspect my-bridge-net

## Results
- Created a custom bridge network.
- Connected Flask, MySQL, and Redis to the network.
- Verified Flask-to-MySQL and Flask-to-Redis connectivity.
- Exposed Flask on host port 5001 without publishing the database ports.

## Cleanup
Remove only the containers created for this exercise:

    docker rm -f ex4-flask ex4-mysql ex4-redis

Remove the custom network after its containers are removed:

    docker network rm my-bridge-net
