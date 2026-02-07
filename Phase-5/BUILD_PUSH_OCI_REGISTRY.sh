#!/bin/bash
# OCI Container Registry - Build and Push Images
# Cloud Shell mein run karein

set -e

echo "=========================================="
echo "  OCI CONTAINER REGISTRY - BUILD & PUSH"
echo "=========================================="
echo ""

# CONFIGURATION - FIXED WITH CORRECT VALUES!
REGION="ca-montreal-1"  # Your region (ca-montreal-1 based on Cloud Shell)
TENANCY_NAMESPACE="axkmnfbutyiu"  # Object Storage Namespace (from: oci os ns get)
OCI_USERNAME="ma9400667@gmail.com"  # OCI Username (from: oci iam user list)
REPO_NAME="todo-app"  # Repository name

# Image names
BACKEND_IMAGE="todo-backend:latest"
FRONTEND_IMAGE="todo-frontend:latest"

# OCI Registry URLs
REGISTRY_URL="${REGION}.ocir.io"
BACKEND_FULL_IMAGE="${REGISTRY_URL}/${TENANCY_NAMESPACE}/${REPO_NAME}/${BACKEND_IMAGE}"
FRONTEND_FULL_IMAGE="${REGISTRY_URL}/${TENANCY_NAMESPACE}/${REPO_NAME}/${FRONTEND_IMAGE}"

echo "Configuration:"
echo "  Region: $REGION"
echo "  Tenancy: $TENANCY_NAMESPACE"
echo "  Registry: $REGISTRY_URL"
echo "  Backend Image: $BACKEND_FULL_IMAGE"
echo "  Frontend Image: $FRONTEND_FULL_IMAGE"
echo ""

# Step 1: Check if project files exist
echo "[1/6] Checking project files..."
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "⚠️  Project files not found in current directory"
    echo "Please upload project files to Cloud Shell or clone repository"
    echo ""
    echo "To upload:"
    echo "  1. Cloud Shell → Upload button"
    echo "  2. Select project folder (phase-4)"
    echo "  3. Upload"
    echo ""
    echo "Or clone:"
    echo "  git clone <your-repo-url>"
    echo "  cd phase-4"
    exit 1
fi
echo "✅ Project files found"
echo ""

# Step 2: Login to OCI Registry
echo "[2/6] Logging in to OCI Container Registry..."

# Construct full username: tenancy-namespace/oci-username
FULL_USERNAME="${TENANCY_NAMESPACE}/${OCI_USERNAME}"
echo "Using OCI username: $FULL_USERNAME"
echo "⚠️  IMPORTANT: Username format = tenancy-namespace/oci-username (NOT email!)"
echo ""

# Try to get token from environment variable first
if [ -z "$OCI_TOKEN" ]; then
    echo "Enter your OCI Auth Token (not password!):"
    echo "  Get it from: Oracle Cloud Console → User Settings → Auth Tokens"
    echo "  Or set environment variable: export OCI_TOKEN='your-token'"
    read OCI_TOKEN
fi

if [ -z "$OCI_TOKEN" ]; then
    echo "❌ OCI Token not provided!"
    echo ""
    echo "Please set: export OCI_TOKEN='your-token'"
    echo "Or run manually: docker login ${REGISTRY_URL} -u ${FULL_USERNAME}"
    exit 1
fi

echo "Attempting login..."
echo "$OCI_TOKEN" | docker login ${REGISTRY_URL} -u ${FULL_USERNAME} --password-stdin 2>&1
LOGIN_RESULT=$?

if [ $LOGIN_RESULT -eq 0 ]; then
    echo "✅ Logged in to OCI Registry successfully!"
else
    echo ""
    echo "❌ Login failed with error code: $LOGIN_RESULT"
    echo ""
    echo "Troubleshooting steps:"
    echo "  1. Verify OCI Username (NOT email!):"
    echo "     OCI Console → Profile → Username"
    echo "     Current: $OCI_USERNAME"
    echo ""
    echo "  2. Verify Auth Token:"
    echo "     OCI Console → User Settings → Auth Tokens"
    echo "     Generate new token if old one expired"
    echo ""
    echo "  3. Verify Tenancy Namespace:"
    echo "     OCI Console → Tenancy Details → Object Storage Namespace"
    echo "     Current: $TENANCY_NAMESPACE"
    echo ""
    echo "  4. Try manual login:"
    echo "     docker login ${REGISTRY_URL} -u ${FULL_USERNAME}"
    echo "     # Password: <your-auth-token>"
    echo ""
    exit 1
fi
echo ""

# Step 3: Build Backend Image
echo "[3/6] Building backend image..."
cd backend
docker build -t ${BACKEND_IMAGE} .
docker tag ${BACKEND_IMAGE} ${BACKEND_FULL_IMAGE}
echo "✅ Backend image built"
cd ..
echo ""

# Step 4: Build Frontend Image
echo "[4/6] Building frontend image..."
cd frontend
docker build -t ${FRONTEND_IMAGE} .
docker tag ${FRONTEND_IMAGE} ${FRONTEND_FULL_IMAGE}
echo "✅ Frontend image built"
cd ..
echo ""

# Step 5: Push Images
echo "[5/6] Pushing images to OCI Registry..."
docker push ${BACKEND_FULL_IMAGE}
docker push ${FRONTEND_FULL_IMAGE}
echo "✅ Images pushed to OCI Registry"
echo ""

# Step 6: Update Deployments
echo "[6/6] Updating Kubernetes deployments..."
kubectl set image deployment/todo-backend backend=${BACKEND_FULL_IMAGE} -n todo-app
kubectl set image deployment/todo-frontend frontend=${FRONTEND_FULL_IMAGE} -n todo-app

echo "✅ Deployments updated"
echo ""

# Wait for pods
echo "Waiting for pods to restart..."
sleep 20
kubectl get pods -n todo-app

echo ""
echo "=========================================="
echo "  ✅ BUILD & PUSH COMPLETE!"
echo "=========================================="
echo ""
echo "Images pushed to:"
echo "  Backend: ${BACKEND_FULL_IMAGE}"
echo "  Frontend: ${FRONTEND_FULL_IMAGE}"
echo ""
echo "Deployments updated. Check status:"
echo "  kubectl get pods -n todo-app"
echo "  kubectl get svc -n todo-app"
echo ""
echo "Access application:"
echo "  http://148.116.94.66:3000"

