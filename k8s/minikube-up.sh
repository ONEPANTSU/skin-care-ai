#!/bin/bash

minikube start

kubectl apply -f k8s/secrets/postgres-secret.yaml
kubectl apply -f k8s/configmaps/postgres-configmap.yaml

kubectl apply -f k8s/volumes/postgres-pv.yaml
kubectl apply -f k8s/volumes/postgres-pvc.yaml

kubectl apply -f k8s/deployments/postgres-deployment.yaml
kubectl apply -f k8s/deployments/postgres-service.yaml

kubectl apply -f k8s/deployments/skincare-cv-deployment.yaml
kubectl apply -f k8s/deployments/skincare-cv-service.yaml

kubectl apply -f k8s/deployments/skincare-genegpt-deployment.yaml
kubectl apply -f k8s/deployments/skincare-genegpt-service.yaml
