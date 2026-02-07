#!/bin/bash
# Deployment script for Kubernetes
# Usage: ./scripts/deploy.sh [install|upgrade|uninstall]

set -e

NAMESPACE="todo-app"
RELEASE_NAME="todo-chatbot"
CHART_PATH="helm/todo-chatbot"

create_namespace() {
    if ! kubectl get namespace $NAMESPACE &> /dev/null; then
        echo "Creating namespace: $NAMESPACE"
        kubectl create namespace $NAMESPACE
    else
        echo "Namespace $NAMESPACE already exists"
    fi
}

create_secrets() {
    echo "Creating secrets..."
    echo "Please ensure you have set the following environment variables:"
    echo "  - DATABASE_URL"
    echo "  - SECRET_KEY"
    echo "  - OPENAI_API_KEY"
    
    if [ -z "$DATABASE_URL" ] || [ -z "$SECRET_KEY" ] || [ -z "$OPENAI_API_KEY" ]; then
        echo "⚠️  Warning: Required environment variables not set"
        echo "Creating secret with empty values (update manually)"
        kubectl create secret generic todo-secrets \
            --from-literal=DATABASE_URL="${DATABASE_URL:-}" \
            --from-literal=SECRET_KEY="${SECRET_KEY:-}" \
            --from-literal=OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
            -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    else
        kubectl create secret generic todo-secrets \
            --from-literal=DATABASE_URL="$DATABASE_URL" \
            --from-literal=SECRET_KEY="$SECRET_KEY" \
            --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
            -n $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    fi
    echo "✓ Secrets created"
}

install() {
    echo "Installing Helm chart..."
    create_namespace
    create_secrets
    
    helm install $RELEASE_NAME $CHART_PATH -n $NAMESPACE
    
    echo "✓ Deployment installed"
    echo ""
    echo "Check status with:"
    echo "  kubectl get pods -n $NAMESPACE"
    echo "  helm status $RELEASE_NAME -n $NAMESPACE"
}

upgrade() {
    echo "Upgrading Helm chart..."
    helm upgrade $RELEASE_NAME $CHART_PATH -n $NAMESPACE
    echo "✓ Deployment upgraded"
}

uninstall() {
    echo "Uninstalling Helm chart..."
    helm uninstall $RELEASE_NAME -n $NAMESPACE
    echo "✓ Deployment uninstalled"
}

case "${1:-install}" in
    install)
        install
        ;;
    upgrade)
        upgrade
        ;;
    uninstall)
        uninstall
        ;;
    *)
        echo "Usage: $0 [install|upgrade|uninstall]"
        exit 1
        ;;
esac

