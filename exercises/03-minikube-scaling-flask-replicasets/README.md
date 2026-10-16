# Exercise 3: Flask Scaling with Kubernetes ReplicaSets

## Objective
Deploy a Flask-based flash sale application on Minikube and demonstrate
replica scaling, automatic Pod replacement, and health checks.

## Technologies
- Python and Flask
- Docker
- Kubernetes ReplicaSet
- Minikube
- Kubernetes Services and HTTP probes

## Application Endpoints
- / : Returns a welcome message, timestamp, and serving Pod hostname.
- /buy?user=Ansh : Simulates a purchase and returns the item, user,
  status, time, and serving Pod hostname.
- /health : Returns the application health status and Pod hostname.

## Files
- app.py: Flask application and HTTP endpoints.
- Dockerfile: Builds the flash sale container image.
- flashsale-replicaset.yaml: ReplicaSet and ClusterIP Service.
- README.md: Setup, testing, and verification instructions.

## Setup

Start the existing Minikube cluster:

    minikube start --driver=docker

Build the Docker image from this directory:

    docker context use desktop-linux
    docker build -t flashsale:1.0 .

Load the image into Minikube:

    minikube image load flashsale:1.0

Deploy the ReplicaSet and Service:

    kubectl apply -f flashsale-replicaset.yaml

## Verify the Initial Replicas

    kubectl get rs flashsale-rs
    kubectl get pods -l app=flashsale
    kubectl get service flashsale-svc

The initial desired replica count is three. The Pods use readiness and
liveness probes on the /health endpoint.

## Scale to Five Replicas

    kubectl scale rs/flashsale-rs --replicas=5
    kubectl get rs flashsale-rs
    kubectl wait --for=condition=Ready pod -l app=flashsale --timeout=120s
    kubectl get pods -l app=flashsale

Expected result: five ready Pods.

## Test Automatic Pod Replacement

Delete one Pod using its actual name:

    kubectl delete pod <pod-name>

Check the ReplicaSet and Pods:

    kubectl get rs flashsale-rs
    kubectl get pods -l app=flashsale

The ReplicaSet should create a replacement and restore the desired count.

## Test the Application

Forward local port 8080 to the ClusterIP Service:

    kubectl port-forward service/flashsale-svc 8080:80

In another terminal, test:

    Invoke-RestMethod http://127.0.0.1:8080/
    Invoke-RestMethod http://127.0.0.1:8080/health
    Invoke-RestMethod "http://127.0.0.1:8080/buy?user=Ansh"

## Results
- Three initial replicas became healthy.
- The ReplicaSet scaled from three to five replicas.
- Deleting a Pod triggered automatic replacement.
- The homepage, health check, and purchase endpoints returned
  successful responses.

## Cleanup

    kubectl delete -f flashsale-replicaset.yaml
