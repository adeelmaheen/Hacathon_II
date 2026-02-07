#!/bin/bash
# Build script for Docker images
# Usage: ./scripts/build-images.sh [backend|frontend|all]

set -e

BACKEND_IMAGE="todo-backend:latest"
FRONTEND_IMAGE="todo-frontend:latest"

build_backend() {
    echo "Building backend image..."
    cd backend
    docker build -t $BACKEND_IMAGE .
    echo "✓ Backend image built: $BACKEND_IMAGE"
    cd ..
}

build_frontend() {
    echo "Building frontend image..."
    cd frontend
    docker build -t $FRONTEND_IMAGE .
    echo "✓ Frontend image built: $FRONTEND_IMAGE"
    cd ..
}

load_to_minikube() {
    if command -v minikube &> /dev/null; then
        echo "Loading images to Minikube..."
        minikube image load $BACKEND_IMAGE
        minikube image load $FRONTEND_IMAGE
        echo "✓ Images loaded to Minikube"
    else
        echo "Minikube not found, skipping image load"
    fi
}

case "${1:-all}" in
    backend)
        build_backend
        ;;
    frontend)
        build_frontend
        ;;
    all)
        build_backend
        build_frontend
        load_to_minikube
        ;;
    *)
        echo "Usage: $0 [backend|frontend|all]"
        exit 1
        ;;
esac

echo "Build complete!"

