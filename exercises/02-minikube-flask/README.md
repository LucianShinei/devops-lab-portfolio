# Exercise 2: Flask on Minikube

## Objective
Containerize a Flask application and deploy it on Kubernetes using Minikube.

## Implementation
- Created a Flask application listening on port 15000.
- Built the Docker image flask-app:latest.
- Loaded the image into Minikube.
- Created a Kubernetes Deployment with one replica.
- Exposed the application using a NodePort Service.

## Files
- app.py: Flask web application.
- Dockerfile: Container image configuration.
- flask-deployment.yaml: Deployment and Service manifests.

## Verification
- Deployment successfully rolled out.
- Flask Pod reached Running status with 1/1 containers ready.
- NodePort Service exposed port 15000.
- Expected application response: Hello from Flask on Kubernetes!

## Cleanup
Run kubectl delete -f flask-deployment.yaml to remove the Deployment and Service.
