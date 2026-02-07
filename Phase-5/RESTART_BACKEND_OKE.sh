#!/bin/bash
# Restart Backend on OKE (Oracle Kubernetes Engine)

echo "=========================================="
echo "   RESTARTING BACKEND ON OKE"
echo "=========================================="
echo ""

# Check if connected to OKE
echo "1️⃣ Checking OKE connection..."
if ! kubectl cluster-info &>/dev/null; then
    echo "❌ Not connected to OKE cluster!"
    echo "   Run: oci ce cluster create-kubeconfig --cluster-id <cluster-id> --region <region>"
    exit 1
fi
echo "✅ Connected to OKE cluster"
echo ""

# Check current pods
echo "2️⃣ Current backend pods:"
kubectl get pods -n todo-app -l app=todo-backend
echo ""

# Restart deployment
echo "3️⃣ Restarting backend deployment..."
kubectl rollout restart deployment/todo-backend -n todo-app

if [ $? -eq 0 ]; then
    echo "✅ Restart command sent successfully"
    echo ""
    
    # Wait for rollout
    echo "4️⃣ Waiting for rollout to complete..."
    kubectl rollout status deployment/todo-backend -n todo-app --timeout=120s
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "5️⃣ New backend pods:"
        kubectl get pods -n todo-app -l app=todo-backend
        echo ""
        echo "=========================================="
        echo "   ✅ BACKEND RESTARTED SUCCESSFULLY!"
        echo "=========================================="
        echo ""
        echo "💡 Check logs:"
        echo "   kubectl logs -n todo-app -l app=todo-backend --tail=50"
        echo ""
    else
        echo ""
        echo "⚠️  Rollout timeout - check pods manually:"
        echo "   kubectl get pods -n todo-app -l app=todo-backend"
        echo ""
    fi
else
    echo "❌ Failed to restart deployment"
    echo "   Check if deployment exists:"
    echo "   kubectl get deployments -n todo-app"
    exit 1
fi

