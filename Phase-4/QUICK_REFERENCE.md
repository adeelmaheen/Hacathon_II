# Quick Reference: Phase IV Deployment Commands

A quick reference card for common Kubernetes deployment commands.

## 🚀 Complete Deployment (Copy & Paste)

```powershell
# 1. Start Minikube
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
minikube addons enable metrics-server

# 2. Build Images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# 3. Load Images
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# 4. Create Namespace
kubectl create namespace todo-app

# 5. Create Secrets (extract from .env)
$envContent = Get-Content backend\.env -Raw
$lines = $envContent -split "`n"
$dbLine = $lines | Where-Object { $_ -match "^DATABASE_URL=" }
if ($dbLine -match "DATABASE_URL=['""](.*)['""]") { $dbUrl = $matches[1] } else { $dbUrl = ($dbLine -split "=", 2)[1].Trim() }
$skLine = $lines | Where-Object { $_ -match "^SECRET_KEY=" }
if ($skLine -match "SECRET_KEY=['""](.*)['""]") { $secretKey = $matches[1] } else { $secretKey = ($skLine -split "=", 2)[1].Trim() }
$oaLine = $lines | Where-Object { $_ -match "^OPENAI_API_KEY=" }
if ($oaLine -match "OPENAI_API_KEY=['""](.*)['""]") { $openaiKey = $matches[1] } else { $openaiKey = ($oaLine -split "=", 2)[1].Trim() }
kubectl create secret generic todo-secrets --from-literal=DATABASE_URL="$dbUrl" --from-literal=SECRET_KEY="$secretKey" --from-literal=OPENAI_API_KEY="$openaiKey" -n todo-app

# 6. Deploy with Helm
cd helm\todo-chatbot
helm install todo-chatbot . -n todo-app --create-namespace

# 7. Verify
kubectl get pods -n todo-app
kubectl get all -n todo-app

# 8. Port Forward (run in separate terminals)
kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app
```

## 📋 Common Commands

### Check Status
```powershell
kubectl get pods -n todo-app
kubectl get svc -n todo-app
kubectl get all -n todo-app
kubectl get deployments -n todo-app
```

### View Logs
```powershell
kubectl logs -l app.kubernetes.io/component=backend -n todo-app
kubectl logs -l app.kubernetes.io/component=frontend -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Restart Services
```powershell
kubectl rollout restart deployment/todo-chatbot-backend -n todo-app
kubectl rollout restart deployment/todo-chatbot-frontend -n todo-app
```

### Scale Deployments
```powershell
kubectl scale deployment todo-chatbot-backend --replicas=3 -n todo-app
kubectl scale deployment todo-chatbot-frontend --replicas=3 -n todo-app
```

### Update Secrets
```powershell
kubectl delete secret todo-secrets -n todo-app
kubectl create secret generic todo-secrets --from-literal=DATABASE_URL="..." --from-literal=SECRET_KEY="..." --from-literal=OPENAI_API_KEY="..." -n todo-app
kubectl rollout restart deployment/todo-chatbot-backend -n todo-app
```

### Port Forwarding
```powershell
# Foreground (blocks terminal)
kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app

# Background (PowerShell)
Start-Job -ScriptBlock { kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app }
Start-Job -ScriptBlock { kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app }
```

### Troubleshooting
```powershell
# Describe pod
kubectl describe pod <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --sort-by=.metadata.creationTimestamp

# Check endpoints
kubectl get endpoints -n todo-app

# Test connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl http://todo-chatbot-backend:8000/health
```

### Helm Commands
```powershell
# Validate chart
helm lint helm/todo-chatbot

# Install
helm install todo-chatbot helm/todo-chatbot -n todo-app

# Upgrade
helm upgrade todo-chatbot helm/todo-chatbot -n todo-app

# Uninstall
helm uninstall todo-chatbot -n todo-app

# Status
helm status todo-chatbot -n todo-app
```

### Minikube Commands
```powershell
# Status
minikube status

# Stop
minikube stop

# Delete
minikube delete

# SSH into Minikube
minikube ssh

# Use Minikube Docker daemon
minikube docker-env | Invoke-Expression
```

## 🧹 Cleanup

```powershell
# Uninstall Helm release
helm uninstall todo-chatbot -n todo-app

# Delete namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Delete Minikube
minikube delete
```

## 🌐 Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health

## 📚 Full Documentation

- **Complete Guide**: [PHASE4_COMPLETE_GUIDE.md](./PHASE4_COMPLETE_GUIDE.md)
- **Deployment Guide**: [PHASE4_DEPLOYMENT.md](./PHASE4_DEPLOYMENT.md)
- **Quick Start**: [QUICK_START_K8S.md](./QUICK_START_K8S.md)

