# Phase IV: Kubernetes Deployment Specification

## Overview
Deploy the Todo Chatbot application to a local Kubernetes cluster using Minikube, with containerization via Docker (using Gordon AI), orchestration via Helm Charts, and AI-assisted operations via kubectl-ai and kagent.

## Objectives
1. Containerize frontend and backend applications using Docker (with Gordon AI assistance)
2. Create Helm charts for Kubernetes deployment
3. Deploy application stack on Minikube
4. Use AI-assisted tools (kubectl-ai, kagent) for Kubernetes operations
5. Ensure production-ready configuration with proper resource management

## Technology Stack

### Containerization
- **Docker Desktop** (4.53+) with Gordon AI Agent enabled
- Multi-stage builds for optimized images
- Docker Compose for local development reference

### Orchestration
- **Minikube** - Local Kubernetes cluster
- **Helm Charts** - Package manager for Kubernetes
- **kubectl** - Kubernetes command-line tool

### AI DevOps Tools
- **kubectl-ai** - AI-assisted kubectl operations
- **kagent** - Advanced Kubernetes AI agent
- **Gordon (Docker AI)** - AI-assisted Docker operations

## Application Components

### Backend Service
- **Technology**: FastAPI (Python 3.13+)
- **Port**: 8000
- **Dependencies**: PostgreSQL database (external - Neon)
- **Environment Variables**:
  - `DATABASE_URL` - PostgreSQL connection string
  - `SECRET_KEY` - JWT secret key
  - `ALGORITHM` - JWT algorithm (default: HS256)
  - `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration (default: 30)
  - `OPENAI_API_KEY` - OpenAI API key for chatbot

### Frontend Service
- **Technology**: Next.js 16 (React 19)
- **Port**: 3000
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL` - Backend API URL

### Database
- **External Service**: Neon PostgreSQL (cloud-hosted)
- **Note**: Database remains external, not containerized

## Containerization Requirements

### Backend Dockerfile
- Base image: Python 3.13-slim
- Use UV package manager for dependencies
- Multi-stage build for optimization
- Health check endpoint: `/health`
- Non-root user for security
- Expose port 8000

### Frontend Dockerfile
- Base image: Node.js 22-alpine
- Multi-stage build (builder + production)
- Static optimization for Next.js
- Health check endpoint: `/api/health` or root
- Non-root user for security
- Expose port 3000

### Docker Images
- Backend image: `todo-backend:latest` (or versioned tag)
- Frontend image: `todo-frontend:latest` (or versioned tag)
- Images should be optimized for size and security

## Kubernetes Deployment Architecture

### Namespace
- **Name**: `todo-app` (or `default`)
- Isolated namespace for application resources

### Backend Deployment
- **Name**: `todo-backend`
- **Replicas**: 2 (for high availability)
- **Resource Limits**:
  - CPU: 500m request, 1000m limit
  - Memory: 512Mi request, 1Gi limit
- **Liveness Probe**: HTTP GET `/health` (interval: 30s)
- **Readiness Probe**: HTTP GET `/health` (interval: 10s)
- **Service**: ClusterIP type, port 8000
- **ConfigMap**: For non-sensitive configuration
- **Secret**: For sensitive data (SECRET_KEY, OPENAI_API_KEY, DATABASE_URL)

### Frontend Deployment
- **Name**: `todo-frontend`
- **Replicas**: 2 (for high availability)
- **Resource Limits**:
  - CPU: 200m request, 500m limit
  - Memory: 256Mi request, 512Mi limit
- **Liveness Probe**: HTTP GET `/` (interval: 30s)
- **Readiness Probe**: HTTP GET `/` (interval: 10s)
- **Service**: ClusterIP type, port 3000
- **ConfigMap**: For NEXT_PUBLIC_API_URL

### Ingress
- **Type**: Ingress resource
- **Backend Service**: todo-backend (port 8000)
- **Frontend Service**: todo-frontend (port 3000)
- **Host**: `todo.local` (or localhost with port-forward)
- **Path-based routing**:
  - `/api/*` → backend service
  - `/*` → frontend service

### Service Discovery
- Backend service accessible at: `http://todo-backend:8000`
- Frontend can reach backend via service name

## Helm Chart Structure

### Chart Name
`todo-chatbot`

### Chart Structure
```
todo-chatbot/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── templates/
│   ├── namespace.yaml  # Namespace definition
│   ├── configmap.yaml # ConfigMaps for both services
│   ├── secret.yaml    # Secrets template
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── hpa.yaml    # Horizontal Pod Autoscaler (optional)
│   ├── frontend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── hpa.yaml    # Horizontal Pod Autoscaler (optional)
│   └── ingress.yaml    # Ingress configuration
└── README.md           # Chart documentation
```

### Helm Values
- Configurable replicas for each service
- Resource limits and requests
- Environment variables
- Image tags and repositories
- Service ports
- Ingress configuration

## Minikube Setup Requirements

### Prerequisites
1. Docker Desktop installed and running
2. Minikube installed
3. kubectl installed
4. Helm 3.x installed
5. kubectl-ai installed
6. kagent installed (optional but recommended)

### Minikube Configuration
- **Driver**: docker (using Docker Desktop)
- **Memory**: Minimum 4GB allocated
- **CPU**: Minimum 2 cores
- **Addons**: 
  - ingress (for Ingress controller)
  - metrics-server (for HPA)

## Deployment Workflow

### Phase 1: Containerization
1. Create Dockerfile for backend (using Gordon AI)
2. Create Dockerfile for frontend (using Gordon AI)
3. Build and test images locally
4. Tag images appropriately
5. Load images into Minikube (or use local registry)

### Phase 2: Helm Chart Creation
1. Initialize Helm chart structure
2. Create backend deployment and service manifests
3. Create frontend deployment and service manifests
4. Create ConfigMap and Secret templates
5. Create Ingress manifest
6. Define values.yaml with defaults
7. Test chart with `helm template` and `helm lint`

### Phase 3: Kubernetes Deployment
1. Start Minikube cluster
2. Enable required addons (ingress, metrics-server)
3. Create namespace
4. Create secrets (DATABASE_URL, SECRET_KEY, OPENAI_API_KEY)
5. Install Helm chart
6. Verify deployments
7. Configure port-forwarding or Ingress for access

### Phase 4: Verification and Testing
1. Check pod status
2. Verify service endpoints
3. Test health checks
4. Test application functionality
5. Monitor resource usage
6. Test scaling operations

## AI-Assisted Operations

### Using kubectl-ai
- Generate deployment manifests
- Troubleshoot pod issues
- Scale deployments
- Check cluster health
- Analyze resource usage

### Using kagent
- Cluster health analysis
- Resource optimization recommendations
- Performance monitoring
- Security scanning

### Using Gordon (Docker AI)
- Generate optimized Dockerfiles
- Troubleshoot build issues
- Optimize image sizes
- Security best practices

## Security Considerations

1. **Secrets Management**: Use Kubernetes Secrets for sensitive data
2. **Non-root Users**: Run containers as non-root users
3. **Resource Limits**: Set appropriate CPU and memory limits
4. **Network Policies**: Consider implementing network policies (optional)
5. **Image Security**: Use minimal base images, scan for vulnerabilities

## Monitoring and Observability

1. **Health Checks**: Liveness and readiness probes
2. **Logs**: Access via `kubectl logs`
3. **Metrics**: Use metrics-server for resource metrics
4. **Status**: Monitor via `kubectl get` commands

## Troubleshooting

### Common Issues
1. Pods in CrashLoopBackOff
2. Services not accessible
3. Image pull errors
4. Resource constraints
5. Network connectivity issues

### Debugging Commands
- `kubectl describe pod <pod-name>`
- `kubectl logs <pod-name>`
- `kubectl exec -it <pod-name> -- /bin/sh`
- `kubectl get events --sort-by=.metadata.creationTimestamp`

## Success Criteria

1. ✅ Both frontend and backend are containerized
2. ✅ Docker images build successfully
3. ✅ Helm chart is created and validated
4. ✅ Application deploys successfully on Minikube
5. ✅ All pods are running and healthy
6. ✅ Services are accessible
7. ✅ Application functionality works end-to-end
8. ✅ Health checks are configured and working
9. ✅ Resource limits are set appropriately
10. ✅ AI tools (kubectl-ai, kagent) are used for operations

## Documentation Requirements

1. **Dockerfiles**: Well-documented with comments
2. **Helm Chart README**: Usage instructions
3. **Deployment Guide**: Step-by-step deployment instructions
4. **Troubleshooting Guide**: Common issues and solutions
5. **AI Tools Usage**: Examples of using kubectl-ai and kagent

## Next Steps After Phase IV

- Production deployment considerations
- CI/CD pipeline integration
- Advanced monitoring (Prometheus, Grafana)
- Service mesh (Istio/Linkerd)
- Advanced scaling strategies

