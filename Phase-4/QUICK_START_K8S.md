# Quick Start: Kubernetes Deployment

This is a quick reference guide for deploying the Todo Chatbot to Minikube.

## Prerequisites Check

```bash
# Verify all tools are installed
docker --version
minikube version
kubectl version --client
helm version
```

## 1. Start Minikube

```bash
# Windows PowerShell
.\scripts\setup-minikube.ps1

# Linux/Mac
./scripts/setup-minikube.sh
```

Or manually:
```bash
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
minikube addons enable metrics-server
```

## 2. Build and Load Images

```bash
# Windows PowerShell
.\scripts\build-images.ps1

# Linux/Mac
./scripts/build-images.sh
```

Or manually:
```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)  # Linux/Mac
minikube docker-env | Invoke-Expression  # Windows PowerShell

# Build images
cd backend && docker build -t todo-backend:latest .
cd ../frontend && docker build -t todo-frontend:latest .

# Reset Docker daemon
eval $(minikube docker-env -u)  # Linux/Mac
```

## 3. Create Secrets

```bash
# Create namespace
kubectl create namespace todo-app

# Create secrets (replace with your actual values)
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="your-postgresql-connection-string" \
  --from-literal=SECRET_KEY="your-super-secret-key-min-32-chars" \
  --from-literal=OPENAI_API_KEY="your-openai-api-key" \
  -n todo-app
```

## 4. Deploy with Helm

```bash
cd helm/todo-chatbot

# Validate chart
helm lint .

# Install
helm install todo-chatbot . -n todo-app

# Check status
kubectl get pods -n todo-app
helm status todo-chatbot -n todo-app
```

## 5. Access Application

### Port Forwarding (Quick Test)

```bash
# Terminal 1: Backend
kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app

# Terminal 2: Frontend
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

### Using Ingress

```bash
# Get Minikube IP
minikube ip

# Add to hosts file
# Windows: C:\Windows\System32\drivers\etc\hosts
# Linux/Mac: /etc/hosts
# <minikube-ip> todo.local

# Access
# Frontend: http://todo.local
# Backend: http://todo.local/api
```

## 6. Verify Deployment

```bash
# Check all resources
kubectl get all -n todo-app

# View logs
kubectl logs -f deployment/todo-chatbot-backend -n todo-app
kubectl logs -f deployment/todo-chatbot-frontend -n todo-app

# Check pod status
kubectl describe pod <pod-name> -n todo-app
```

## Using AI Tools

### kubectl-ai

```bash
# Check cluster health
kubectl-ai "check the health of all pods in todo-app namespace"

# Scale deployment
kubectl-ai "scale todo-chatbot-backend to 3 replicas in todo-app namespace"

# Troubleshoot
kubectl-ai "why are pods failing in todo-app namespace?"
```

### kagent

```bash
# Analyze cluster
kagent "analyze the health of todo-app namespace"

# Optimize resources
kagent "optimize resource allocation for todo-chatbot"
```

## Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
kubectl get events -n todo-app --sort-by=.metadata.creationTimestamp
```

### Service Not Accessible

```bash
# Check endpoints
kubectl get endpoints -n todo-app

# Test from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl http://todo-chatbot-backend:8000/health
```

## Cleanup

```bash
# Uninstall
helm uninstall todo-chatbot -n todo-app

# Delete namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Delete cluster
minikube delete
```

## Next Steps

- See [PHASE4_DEPLOYMENT.md](./PHASE4_DEPLOYMENT.md) for detailed documentation
- See [helm/todo-chatbot/README.md](./helm/todo-chatbot/README.md) for Helm chart details

