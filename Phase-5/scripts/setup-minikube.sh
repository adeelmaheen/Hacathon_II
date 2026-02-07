#!/bin/bash
# Minikube setup script
# Usage: ./scripts/setup-minikube.sh

set -e

echo "Setting up Minikube cluster..."

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed"
    echo "Install from: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if Minikube is already running
if minikube status &> /dev/null; then
    echo "Minikube is already running"
    read -p "Do you want to restart it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopping Minikube..."
        minikube stop
        minikube delete
    else
        echo "Using existing Minikube cluster"
        exit 0
    fi
fi

# Start Minikube
echo "Starting Minikube cluster..."
minikube start --driver=docker --memory=4096 --cpus=2

# Enable addons
echo "Enabling required addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Verify addons
echo "Verifying addons..."
minikube addons list

# Get cluster info
echo ""
echo "✓ Minikube cluster is ready!"
echo ""
echo "Cluster info:"
kubectl cluster-info

echo ""
echo "Minikube IP:"
minikube ip

echo ""
echo "To use Minikube's Docker daemon:"
echo "  eval \$(minikube docker-env)"

