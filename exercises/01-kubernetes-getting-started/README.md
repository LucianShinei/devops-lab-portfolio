# Exercise 1: Kubernetes Getting Started

## Objective
Deploy an Nginx web server on a local Kubernetes cluster and expose it using a NodePort Service.

## Prerequisites
- Docker Desktop
- kubectl
- Minikube

## Implementation
- Started a local Kubernetes cluster using Minikube.
- Deployed an Nginx Pod named hello-k8s.
- Exposed port 80 using a NodePort Service.
- Verified the Nginx welcome page in a browser.

## Commands Used
- Start cluster: minikube start --driver=docker
- Check nodes: kubectl get nodes
- Check pods: kubectl get pods
- Check services: kubectl get services
- Open application: minikube service hello-k8s

## Files
- pod.yaml: Kubernetes Pod manifest.
- service.yaml: NodePort Service manifest.

## Expected Result
The Pod reaches Running status, the Service exposes port 80 through a NodePort, and the browser displays the Nginx welcome page.

## Cleanup
- kubectl delete -f service.yaml
- kubectl delete -f pod.yaml
