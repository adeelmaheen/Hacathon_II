#!/bin/bash
# Setup Dapr on Minikube
# Usage: ./scripts/setup-dapr-minikube.sh

set -e

echo "Setting up Dapr on Minikube..."

# Check if Dapr CLI is installed
if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr CLI is not installed"
    echo "Install from: https://docs.dapr.io/getting-started/install-dapr-cli/"
    exit 1
fi

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    echo "❌ Minikube is not running"
    echo "Start Minikube first: minikube start"
    exit 1
fi

# Initialize Dapr on Kubernetes
echo "Initializing Dapr on Kubernetes..."
dapr init -k

# Wait for Dapr to be ready
echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s

# Apply Dapr components
echo "Applying Dapr components..."
kubectl apply -f dapr/components/

# Verify Dapr installation
echo ""
echo "✓ Dapr installed successfully!"
echo ""
echo "Dapr system pods:"
kubectl get pods -n dapr-system

echo ""
echo "Dapr components:"
kubectl get components -n default

echo ""
echo "To use Dapr in your application, add annotations to your deployment:"
echo "  annotations:"
echo "    dapr.io/enabled: \"true\""
echo "    dapr.io/app-id: \"todo-backend\""
echo "    dapr.io/app-port: \"8000\""

