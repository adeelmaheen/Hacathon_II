# Todo Chatbot Helm Chart

This Helm chart deploys the Todo Chatbot application (Frontend + Backend) to a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Minikube (for local development)

## Installation

### Quick Start

```bash
# Create namespace
kubectl create namespace todo-app

# Create secrets
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="your-database-url" \
  --from-literal=SECRET_KEY="your-secret-key" \
  --from-literal=OPENAI_API_KEY="your-openai-key" \
  -n todo-app

# Install chart
helm install todo-chatbot . -n todo-app
```

### Using Custom Values

```bash
# Install with custom values file
helm install todo-chatbot . -f my-values.yaml -n todo-app

# Or override specific values
helm install todo-chatbot . \
  --set backend.replicaCount=3 \
  --set frontend.replicaCount=3 \
  -n todo-app
```

## Configuration

### Values File

The default values are in `values.yaml`. Key configuration options:

#### Backend
- `backend.replicaCount`: Number of backend replicas (default: 2)
- `backend.image.repository`: Backend image repository
- `backend.image.tag`: Backend image tag
- `backend.resources`: Resource limits and requests

#### Frontend
- `frontend.replicaCount`: Number of frontend replicas (default: 2)
- `frontend.image.repository`: Frontend image repository
- `frontend.image.tag`: Frontend image tag
- `frontend.resources`: Resource limits and requests

#### Ingress
- `ingress.enabled`: Enable Ingress (default: true)
- `ingress.hosts`: Ingress host configuration
- `ingress.className`: Ingress class name

### Secrets

Secrets should be created separately before installation:

```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="..." \
  --from-literal=SECRET_KEY="..." \
  --from-literal=OPENAI_API_KEY="..." \
  -n todo-app
```

Then update the deployment template to reference this secret, or set `secrets.create: true` in values.yaml (not recommended for production).

## Upgrading

```bash
# Upgrade with same values
helm upgrade todo-chatbot . -n todo-app

# Upgrade with new values
helm upgrade todo-chatbot . -f new-values.yaml -n todo-app
```

## Uninstalling

```bash
helm uninstall todo-chatbot -n todo-app
```

## Verification

```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check deployments
kubectl get deployments -n todo-app

# View logs
kubectl logs -f deployment/todo-chatbot-backend -n todo-app
kubectl logs -f deployment/todo-chatbot-frontend -n todo-app
```

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod
kubectl describe pod <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --sort-by=.metadata.creationTimestamp
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# Port forward for testing
kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app
```

## Chart Structure

```
todo-chatbot/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default values
├── README.md               # This file
└── templates/
    ├── _helpers.tpl        # Template helpers
    ├── namespace.yaml      # Namespace definition
    ├── backend/
    │   ├── configmap.yaml  # Backend ConfigMap
    │   ├── secret.yaml     # Backend Secret (optional)
    │   ├── deployment.yaml # Backend Deployment
    │   └── service.yaml    # Backend Service
    ├── frontend/
    │   ├── configmap.yaml  # Frontend ConfigMap
    │   ├── deployment.yaml # Frontend Deployment
    │   └── service.yaml    # Frontend Service
    └── ingress.yaml        # Ingress configuration
```

## Support

For issues and questions, please refer to the main project documentation or create an issue in the repository.

