# Phase IV: Kubernetes Deployment Guide

This guide walks you through deploying the Todo Chatbot application to a local Kubernetes cluster using Minikube.

## Prerequisites

### Required Software
1. **Docker Desktop 4.53+** (with Gordon AI Agent enabled)
   - Download from: https://www.docker.com/products/docker-desktop
   - Enable Gordon: Settings > Beta features > Toggle "Docker AI Agent"
   
2. **Minikube**
   - Install: https://minikube.sigs.k8s.io/docs/start/
   - Windows: `choco install minikube` or download from GitHub releases
   
3. **kubectl**
   - Install: https://kubernetes.io/docs/tasks/tools/
   - Windows: `choco install kubernetes-cli`
   
4. **Helm 3.x**
   - Install: https://helm.sh/docs/intro/install/
   - Windows: `choco install kubernetes-helm`

### AI DevOps Tools (Optional but Recommended)
1. **kubectl-ai**
   - Install: `npm install -g kubectl-ai`
   - Or: `pip install kubectl-ai`
   
2. **kagent**
   - Install: Follow instructions at https://github.com/kagent-ai/kagent

### Verify Installations
```bash
docker --version
minikube version
kubectl version --client
helm version
```

## Step 1: Build Docker Images

### Option A: Using Gordon AI Agent (Recommended)

#### Backend Image
```bash
# Navigate to backend directory
cd backend

# Use Gordon to help build (if available)
docker ai "build a Docker image for this FastAPI application with Python 3.13, using UV package manager, with health checks"

# Or build manually
docker build -t todo-backend:latest .
```

#### Frontend Image
```bash
# Navigate to frontend directory
cd frontend

# Use Gordon to help build (if available)
docker ai "build a Docker image for this Next.js application with Node.js 22, optimized for production"

# Or build manually
docker build -t todo-frontend:latest .
```

### Option B: Manual Build

#### Build Backend
```bash
cd backend
docker build -t todo-backend:latest .
```

#### Build Frontend
```bash
cd frontend
docker build -t todo-frontend:latest .
```

### Test Images Locally
```bash
# Test backend
docker run -p 8000:8000 \
  -e DATABASE_URL="your-database-url" \
  -e SECRET_KEY="your-secret-key" \
  -e OPENAI_API_KEY="your-openai-key" \
  todo-backend:latest

# Test frontend
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
  todo-frontend:latest
```

## Step 2: Start Minikube

```bash
# Start Minikube cluster
minikube start --driver=docker --memory=4096 --cpus=2

# Verify cluster is running
kubectl cluster-info

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify addons
minikube addons list
```

## Step 3: Load Images into Minikube

Since Minikube uses its own Docker daemon, you need to load images:

```bash
# Load backend image
minikube image load todo-backend:latest

# Load frontend image
minikube image load todo-frontend:latest

# Verify images are loaded
minikube image ls
```

**Alternative**: Use Minikube's Docker daemon directly:
```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images directly in Minikube
cd backend && docker build -t todo-backend:latest .
cd ../frontend && docker build -t todo-frontend:latest .

# Reset Docker daemon
eval $(minikube docker-env -u)
```

## Step 4: Create Kubernetes Secrets

Create secrets for sensitive data (database URL, secret key, OpenAI API key):

```bash
# Create namespace (if using custom namespace)
kubectl create namespace todo-app

# Create secrets
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="your-postgresql-connection-string" \
  --from-literal=SECRET_KEY="your-super-secret-key-min-32-chars" \
  --from-literal=OPENAI_API_KEY="your-openai-api-key" \
  -n todo-app
```

**Note**: Update the Helm chart to reference this secret name, or use the chart's secret creation feature.

## Step 5: Deploy with Helm

### Validate Helm Chart
```bash
cd helm/todo-chatbot

# Lint the chart
helm lint .

# Dry-run to see what will be deployed
helm install todo-chatbot . --dry-run --debug -n todo-app
```

### Install the Chart
```bash
# Install the chart
helm install todo-chatbot . -n todo-app

# Or install with custom values
helm install todo-chatbot . -f values.yaml -n todo-app

# Check deployment status
helm status todo-chatbot -n todo-app
```

### Verify Deployment
```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check deployments
kubectl get deployments -n todo-app

# View pod logs
kubectl logs -f deployment/todo-chatbot-backend -n todo-app
kubectl logs -f deployment/todo-chatbot-frontend -n todo-app
```

## Step 6: Access the Application

### Option A: Port Forwarding (Quick Test)

```bash
# Forward backend port
kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app

# Forward frontend port (in another terminal)
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

### Option B: Ingress (Production-like)

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (or C:\Windows\System32\drivers\etc\hosts on Windows)
# <minikube-ip> todo.local

# Access via Ingress
# Frontend: http://todo.local
# Backend API: http://todo.local/api
```

## Step 7: Using AI-Assisted Tools

### kubectl-ai Examples

```bash
# Check cluster health
kubectl-ai "check the health of all pods in todo-app namespace"

# Scale backend
kubectl-ai "scale the todo-chatbot-backend deployment to 3 replicas in todo-app namespace"

# Troubleshoot issues
kubectl-ai "why are the pods in todo-app namespace failing?"

# Get resource usage
kubectl-ai "show me the resource usage of all pods in todo-app namespace"
```

### kagent Examples

```bash
# Analyze cluster health
kagent "analyze the health of the todo-app namespace"

# Optimize resources
kagent "optimize resource allocation for the todo-chatbot deployment"

# Performance analysis
kagent "analyze performance metrics for todo-app namespace"
```

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod to see events
kubectl describe pod <pod-name> -n todo-app

# Check logs
kubectl logs <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --sort-by=.metadata.creationTimestamp
```

### Image Pull Errors

```bash
# Verify images are loaded
minikube image ls

# Reload images if needed
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# Test service from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl http://todo-chatbot-backend:8000/health
```

### Resource Constraints

```bash
# Check resource usage
kubectl top pods -n todo-app

# Adjust resources in values.yaml and upgrade
helm upgrade todo-chatbot . -n todo-app
```

## Updating the Deployment

### Update Images

```bash
# Rebuild and load new images
docker build -t todo-backend:v0.2.0 ./backend
minikube image load todo-backend:v0.2.0

# Update Helm values
# Edit values.yaml to use new tag: v0.2.0

# Upgrade deployment
helm upgrade todo-chatbot . -n todo-app
```

### Update Configuration

```bash
# Edit values.yaml
# Then upgrade
helm upgrade todo-chatbot . -n todo-app

# Or use --set flag
helm upgrade todo-chatbot . --set backend.replicaCount=3 -n todo-app
```

## Scaling

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment todo-chatbot-backend --replicas=3 -n todo-app

# Scale frontend
kubectl scale deployment todo-chatbot-frontend --replicas=3 -n todo-app
```

### Using kubectl-ai

```bash
kubectl-ai "scale todo-chatbot-backend to 4 replicas in todo-app namespace"
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-chatbot -n todo-app

# Delete namespace (if created)
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Next Steps

1. **Production Considerations**:
   - Use proper image registry (Docker Hub, ECR, GCR)
   - Implement proper secret management (External Secrets Operator)
   - Set up monitoring (Prometheus, Grafana)
   - Configure autoscaling (HPA)

2. **CI/CD Integration**:
   - Automate image builds
   - Automate Helm deployments
   - Implement GitOps (ArgoCD, Flux)

3. **Advanced Features**:
   - Service mesh (Istio, Linkerd)
   - Advanced networking policies
   - Multi-environment deployments

## Additional Resources

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl-ai GitHub](https://github.com/kubectl-ai/kubectl-ai)
- [kagent Documentation](https://kagent.ai/docs)

