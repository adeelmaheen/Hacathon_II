#!/bin/bash
# Setup script for Oracle Cloud OKE deployment
# Usage: ./scripts/setup-oke.sh

set -e

echo "Setting up Oracle Cloud OKE deployment..."

# Check prerequisites
command -v kubectl >/dev/null 2>&1 || { echo "kubectl is required but not installed. Aborting." >&2; exit 1; }
command -v helm >/dev/null 2>&1 || { echo "helm is required but not installed. Aborting." >&2; exit 1; }
command -v dapr >/dev/null 2>&1 || { echo "dapr CLI is required but not installed. Aborting." >&2; exit 1; }

# Variables (update these)
CLUSTER_OCID="${CLUSTER_OCID:-}"
OCI_REGION="${OCI_REGION:-us-ashburn-1}"
NAMESPACE="${NAMESPACE:-todo-app}"

if [ -z "$CLUSTER_OCID" ]; then
    echo "Error: CLUSTER_OCID environment variable not set"
    echo "Get it from: OCI Console → OKE → Your Cluster → Cluster Information"
    exit 1
fi

echo "Configuring kubectl for OKE cluster..."
oci ce cluster create-kubeconfig \
    --cluster-id "$CLUSTER_OCID" \
    --file "$HOME/.kube/config" \
    --region "$OCI_REGION" \
    --token-version 2.0.0

echo "Verifying cluster connection..."
kubectl get nodes

echo "Installing Dapr on OKE..."
dapr init -k

echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s

echo "Creating namespace..."
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

echo "Applying Dapr components..."
kubectl apply -f dapr/components/
kubectl apply -f dapr/configurations/

echo "Verifying Dapr installation..."
kubectl get pods -n dapr-system
kubectl get components -n default

echo ""
echo "✅ OKE setup complete!"
echo ""
echo "Next steps:"
echo "1. Create secrets: kubectl create secret generic todo-secrets ... -n $NAMESPACE"
echo "2. Update Helm values with your image registry"
echo "3. Deploy: helm install todo-chatbot helm/todo-chatbot -n $NAMESPACE"

