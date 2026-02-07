# Phase IV: Complete Kubernetes Deployment Guide (A to Z)

This is a comprehensive, step-by-step guide to deploy the Todo Chatbot application to Kubernetes using Minikube. Every command is explained in detail.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Verify Installations](#step-1-verify-installations)
3. [Step 2: Start Minikube Cluster](#step-2-start-minikube-cluster)
4. [Step 3: Build Docker Images](#step-3-build-docker-images)
5. [Step 4: Load Images into Minikube](#step-4-load-images-into-minikube)
6. [Step 5: Create Kubernetes Namespace](#step-5-create-kubernetes-namespace)
7. [Step 6: Create Kubernetes Secrets](#step-6-create-kubernetes-secrets)
8. [Step 7: Deploy with Helm](#step-7-deploy-with-helm)
9. [Step 8: Verify Deployment](#step-8-verify-deployment)
10. [Step 9: Access the Application](#step-9-access-the-application)
11. [Step 10: Troubleshooting](#step-10-troubleshooting)
12. [Cleanup Commands](#cleanup-commands)

---

## Prerequisites

Before starting, ensure you have the following installed:

### Required Software

1. **Docker Desktop 4.53+**
   - Download: https://www.docker.com/products/docker-desktop
   - Enable Gordon AI (optional): Settings > Beta features > Docker AI Agent

2. **Minikube**
   - Windows: `choco install minikube` or download from https://minikube.sigs.k8s.io/docs/start/
   - Verify: `minikube version`

3. **kubectl** (Kubernetes CLI)
   - Windows: `choco install kubernetes-cli`
   - Or download from: https://kubernetes.io/docs/tasks/tools/

4. **Helm 3.x** (Kubernetes Package Manager)
   - Windows: `choco install kubernetes-helm`
   - Or download from: https://helm.sh/docs/intro/install/

### Optional AI Tools

- **kubectl-ai**: `npm install -g kubectl-ai` or `pip install kubectl-ai`
- **kagent**: Follow instructions at https://github.com/kagent-ai/kagent

---

## Step 1: Verify Installations

**What we're doing:** Check that all required tools are installed and working.

```powershell
# Check Docker version
docker --version
# Expected output: Docker version 29.x.x or higher

# Check Minikube version
minikube version
# Expected output: minikube version: v1.38.0 or higher

# Check kubectl version
kubectl version --client
# Expected output: Client Version: v1.34.x or higher

# Check Helm version
helm version
# Expected output: version.BuildInfo{Version:"v4.x.x", ...}
```

**Explanation:**
- These commands verify that all tools are installed and accessible
- If any command fails, install the missing tool before proceeding

---

## Step 2: Start Minikube Cluster

**What we're doing:** Create and start a local Kubernetes cluster using Minikube.

### 2.1 Check if Minikube is already running

```powershell
# Check Minikube status
minikube status
```

**Explanation:**
- If Minikube is already running, you'll see "Running" status
- If not running or doesn't exist, proceed to start it

### 2.2 Start Minikube (if not running)

```powershell
# Start Minikube with specific resources
minikube start --driver=docker --memory=4096 --cpus=2
```

**Explanation:**
- `--driver=docker`: Use Docker as the virtualization driver (requires Docker Desktop)
- `--memory=4096`: Allocate 4GB RAM to the Minikube VM
- `--cpus=2`: Allocate 2 CPU cores
- This creates a single-node Kubernetes cluster on your machine

**Expected output:**
```
😄  minikube v1.38.0 on Microsoft Windows 11
✨  Using the docker driver based on existing profile
👍  Starting "minikube" primary control-plane node
...
🏄  Done! kubectl is now configured to use "minikube" cluster
```

### 2.3 Enable Required Addons

```powershell
# Enable Ingress controller (for routing external traffic)
minikube addons enable ingress

# Enable metrics-server (for resource monitoring and HPA)
minikube addons enable metrics-server
```

**Explanation:**
- **Ingress**: Allows external access to services via HTTP/HTTPS
- **Metrics-server**: Collects resource usage data (CPU, memory) for pods and nodes
- These addons are essential for production-like deployments

### 2.4 Verify Cluster Status

```powershell
# Check cluster information
kubectl cluster-info

# Check nodes
kubectl get nodes

# Verify addons are enabled
minikube addons list
```

**Explanation:**
- `kubectl cluster-info`: Shows the Kubernetes API server URL
- `kubectl get nodes`: Lists all nodes in the cluster (should show "minikube")
- `minikube addons list`: Shows which addons are enabled (ingress and metrics-server should be enabled)

---

## Step 3: Build Docker Images

**What we're doing:** Create Docker images for the frontend and backend applications.

### 3.1 Navigate to Project Directory

```powershell
# Navigate to the project root
cd C:\Users\ma940\Desktop\hackathon-2\phase-4
```

**Explanation:**
- Change to the project directory where the Dockerfiles are located

### 3.2 Build Backend Image

```powershell
# Build the backend Docker image
docker build -t todo-backend:latest ./backend
```

**Explanation:**
- `docker build`: Command to build a Docker image
- `-t todo-backend:latest`: Tag the image with name "todo-backend" and tag "latest"
- `./backend`: Path to the directory containing the Dockerfile
- This creates a multi-stage build optimized for production

**What happens:**
1. Downloads Python 3.13-slim base image
2. Installs UV package manager
3. Installs Python dependencies
4. Copies application code
5. Creates a production-ready image with non-root user

**Expected output:**
```
[+] Building 102.9s (17/17) FINISHED
 => [internal] load build definition from Dockerfile
 => [builder 1/6] FROM docker.io/library/python:3.13-slim
 ...
 => exporting to image
 => naming to docker.io/library/todo-backend:latest
```

### 3.3 Build Frontend Image

```powershell
# Build the frontend Docker image
docker build -t todo-frontend:latest ./frontend
```

**Explanation:**
- Similar to backend, but builds the Next.js frontend
- Uses Node.js 22-alpine as base image
- Creates a standalone Next.js production build

**Expected output:**
```
[+] Building 101.8s (17/17) FINISHED
 => [deps 1/4] FROM docker.io/library/node:22-alpine
 ...
 => exporting to image
 => naming to docker.io/library/todo-frontend:latest
```

### 3.4 Verify Images are Built

```powershell
# List all Docker images
docker images | Select-String "todo"
```

**Explanation:**
- Lists all Docker images and filters for "todo"
- Should show both `todo-backend:latest` and `todo-frontend:latest`

**Expected output:**
```
todo-backend    latest    abc123def456    2 minutes ago    450MB
todo-frontend   latest    def456abc123    1 minute ago     180MB
```

---

## Step 4: Load Images into Minikube

**What we're doing:** Make the Docker images available to Minikube's Kubernetes cluster.

**Why this is needed:**
- Minikube has its own Docker daemon (separate from Docker Desktop)
- Images built in Docker Desktop are not automatically available to Minikube
- We need to load them into Minikube's Docker daemon

### 4.1 Load Backend Image

```powershell
# Load backend image into Minikube
minikube image load todo-backend:latest
```

**Explanation:**
- `minikube image load`: Copies the image from Docker Desktop to Minikube's Docker daemon
- This makes the image available for Kubernetes pods to use

### 4.2 Load Frontend Image

```powershell
# Load frontend image into Minikube
minikube image load todo-frontend:latest
```

**Explanation:**
- Same process for the frontend image

### 4.3 Verify Images are Loaded

```powershell
# List images in Minikube
minikube image ls | Select-String "todo"
```

**Explanation:**
- Lists all images available in Minikube
- Should show both todo-backend and todo-frontend

**Alternative method (using Minikube's Docker daemon):**

```powershell
# Use Minikube's Docker daemon
minikube docker-env | Invoke-Expression

# Now list images (this shows Minikube's images)
docker images | Select-String "todo"

# Reset to regular Docker daemon
minikube docker-env -u | Invoke-Expression
```

**Explanation:**
- `minikube docker-env`: Returns commands to configure Docker to use Minikube's daemon
- `Invoke-Expression`: Executes those commands in PowerShell
- After this, `docker` commands affect Minikube's Docker, not Docker Desktop

---

## Step 5: Create Kubernetes Namespace

**What we're doing:** Create an isolated namespace for our application.

**Why namespaces?**
- Organize resources (pods, services, etc.)
- Isolate applications from each other
- Apply resource quotas and policies

```powershell
# Create namespace (Helm will create it, but we can pre-create)
kubectl create namespace todo-app
```

**Explanation:**
- `kubectl create namespace`: Creates a new Kubernetes namespace
- `todo-app`: Name of the namespace
- All our application resources will be deployed in this namespace

**Verify namespace:**

```powershell
# List all namespaces
kubectl get namespaces

# Or use short form
kubectl get ns
```

**Expected output:**
```
NAME              STATUS   AGE
default           Active   30m
kube-system       Active   30m
kube-public       Active   30m
kube-node-lease   Active   30m
todo-app          Active   5s
```

---

## Step 6: Create Kubernetes Secrets

**What we're doing:** Store sensitive configuration data (database URL, API keys) securely.

**Why secrets?**
- Kubernetes Secrets encrypt sensitive data at rest
- Keeps credentials out of code and configuration files
- Can be mounted as files or environment variables in pods

### 6.1 Read Values from .env File

First, let's check what values we need:

```powershell
# View backend .env file (to see what values we need)
Get-Content backend\.env
```

**Explanation:**
- Shows the environment variables needed
- We need: DATABASE_URL, SECRET_KEY, OPENAI_API_KEY

### 6.2 Extract Values from .env File

```powershell
# Read .env file and extract values
$envContent = Get-Content backend\.env -Raw
$lines = $envContent -split "`n"

# Extract DATABASE_URL (handles both quoted and unquoted values)
$dbLine = $lines | Where-Object { $_ -match "^DATABASE_URL=" }
if ($dbLine -match "DATABASE_URL=['""](.*)['""]") {
    $dbUrl = $matches[1]
} else {
    $dbUrl = ($dbLine -split "=", 2)[1].Trim()
}

# Extract SECRET_KEY
$skLine = $lines | Where-Object { $_ -match "^SECRET_KEY=" }
if ($skLine -match "SECRET_KEY=['""](.*)['""]") {
    $secretKey = $matches[1]
} else {
    $secretKey = ($skLine -split "=", 2)[1].Trim()
}

# Extract OPENAI_API_KEY
$oaLine = $lines | Where-Object { $_ -match "^OPENAI_API_KEY=" }
if ($oaLine -match "OPENAI_API_KEY=['""](.*)['""]") {
    $openaiKey = $matches[1]
} else {
    $openaiKey = ($oaLine -split "=", 2)[1].Trim()
}

# Display extracted values (first 30 chars for security)
Write-Host "DATABASE_URL: $($dbUrl.Substring(0, [Math]::Min(30, $dbUrl.Length)))..."
Write-Host "SECRET_KEY: $($secretKey.Substring(0, [Math]::Min(10, $secretKey.Length)))..."
Write-Host "OPENAI_API_KEY: $($openaiKey.Substring(0, [Math]::Min(10, $openaiKey.Length)))..."
```

**Explanation:**
- Reads the .env file and extracts values
- Handles both quoted (`DATABASE_URL='value'`) and unquoted (`DATABASE_URL=value`) formats
- Stores values in PowerShell variables for use in the next step

### 6.3 Create Kubernetes Secret

```powershell
# Create secret with extracted values
kubectl create secret generic todo-secrets `
  --from-literal=DATABASE_URL="$dbUrl" `
  --from-literal=SECRET_KEY="$secretKey" `
  --from-literal=OPENAI_API_KEY="$openaiKey" `
  -n todo-app
```

**Explanation:**
- `kubectl create secret generic`: Creates a generic secret (not tied to a specific service account)
- `todo-secrets`: Name of the secret
- `--from-literal=KEY=value`: Adds a key-value pair to the secret
- `-n todo-app`: Creates the secret in the todo-app namespace
- Values are base64 encoded automatically by Kubernetes

**Alternative (manual method):**

If you prefer to enter values manually:

```powershell
kubectl create secret generic todo-secrets `
  --from-literal=DATABASE_URL="your-postgresql-connection-string" `
  --from-literal=SECRET_KEY="your-super-secret-key-min-32-chars" `
  --from-literal=OPENAI_API_KEY="your-openai-api-key" `
  -n todo-app
```

### 6.4 Verify Secret was Created

```powershell
# List secrets in namespace
kubectl get secrets -n todo-app

# View secret details (values are base64 encoded)
kubectl get secret todo-secrets -n todo-app -o yaml
```

**Explanation:**
- `kubectl get secrets`: Lists all secrets in the namespace
- `-o yaml`: Shows full YAML definition
- Values are base64 encoded (not plain text) for security

**Expected output:**
```
NAME           TYPE     DATA   AGE
todo-secrets   Opaque   3      10s
```

---

## Step 7: Deploy with Helm

**What we're doing:** Deploy the application using Helm charts (Kubernetes package manager).

**Why Helm?**
- Manages complex Kubernetes deployments
- Templates allow configuration reuse
- Easy upgrades and rollbacks
- Standard way to package Kubernetes applications

### 7.1 Navigate to Helm Chart Directory

```powershell
# Navigate to Helm chart directory
cd helm\todo-chatbot
```

**Explanation:**
- Helm charts are in the `helm/todo-chatbot` directory

### 7.2 Validate Helm Chart

```powershell
# Lint the Helm chart (check for errors)
helm lint .
```

**Explanation:**
- `helm lint`: Validates the chart structure and templates
- Checks for syntax errors, missing values, etc.
- Should return "0 chart(s) failed" if everything is correct

**Expected output:**
```
==> Linting helm/todo-chatbot
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```

### 7.3 Dry Run (Preview Deployment)

```powershell
# Preview what will be deployed (without actually deploying)
helm install todo-chatbot . -n todo-app --dry-run --debug
```

**Explanation:**
- `helm install`: Command to install a chart
- `todo-chatbot`: Name of the release (what you'll call this deployment)
- `.`: Current directory (where the chart is)
- `-n todo-app`: Deploy to todo-app namespace
- `--dry-run`: Simulate the installation without actually creating resources
- `--debug`: Show detailed output including rendered templates

**What this shows:**
- All Kubernetes resources that will be created
- Rendered YAML with actual values
- Helps catch errors before deployment

### 7.4 Install the Helm Chart

```powershell
# Install the Helm chart
helm install todo-chatbot . -n todo-app --create-namespace
```

**Explanation:**
- `--create-namespace`: Creates the namespace if it doesn't exist (we already created it, but this is safe)
- This actually creates all the Kubernetes resources (deployments, services, configmaps, etc.)

**Expected output:**
```
NAME: todo-chatbot
LAST DEPLOYED: Wed Feb  4 13:33:52 2026
NAMESPACE: todo-app
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
```

### 7.5 Verify Helm Installation

```powershell
# Check Helm release status
helm status todo-chatbot -n todo-app

# List all Helm releases
helm list -n todo-app
```

**Explanation:**
- `helm status`: Shows detailed status of a release
- `helm list`: Lists all Helm releases in the namespace

---

## Step 8: Verify Deployment

**What we're doing:** Check that all resources were created and pods are running.

### 8.1 Check Pods

```powershell
# List all pods in the namespace
kubectl get pods -n todo-app
```

**Explanation:**
- Shows all pods (containers) in the namespace
- Status should be "Running" and READY should be "1/1" or "2/2"

**Expected output:**
```
NAME                                     READY   STATUS    RESTARTS   AGE
todo-chatbot-backend-67446bd7dd-fgdqj    1/1     Running   0          2m
todo-chatbot-backend-67446bd7dd-n57f8     1/1     Running   0          2m
todo-chatbot-frontend-77c7f7b844-5swrm   1/1     Running   0          2m
todo-chatbot-frontend-77c7f7b844-xg6dm   1/1     Running   0          2m
```

**What the columns mean:**
- **NAME**: Pod name (includes deployment name and unique ID)
- **READY**: Number of ready containers / total containers (1/1 = ready)
- **STATUS**: Current state (Running, Pending, Error, etc.)
- **RESTARTS**: Number of times the container has restarted
- **AGE**: How long the pod has been running

### 8.2 Check Services

```powershell
# List all services
kubectl get svc -n todo-app
```

**Explanation:**
- Services provide stable network endpoints for pods
- Type "ClusterIP" means they're only accessible within the cluster

**Expected output:**
```
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
todo-chatbot-backend    ClusterIP   10.99.155.179   <none>        8000/TCP   2m
todo-chatbot-frontend   ClusterIP   10.110.42.50    <none>        3000/TCP   2m
```

### 8.3 Check Deployments

```powershell
# List all deployments
kubectl get deployments -n todo-app
```

**Explanation:**
- Deployments manage pod replicas
- Shows desired vs. actual replica count

**Expected output:**
```
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
todo-chatbot-backend    2/2     2            2           2m
todo-chatbot-frontend   2/2     2            2           2m
```

**What the columns mean:**
- **READY**: Ready replicas / desired replicas
- **UP-TO-DATE**: Replicas updated to latest version
- **AVAILABLE**: Replicas available for traffic

### 8.4 Check All Resources

```powershell
# Get all resources at once
kubectl get all -n todo-app
```

**Explanation:**
- Shows pods, services, deployments, and replicasets in one view
- Quick way to see overall status

### 8.5 View Pod Logs

```powershell
# View backend logs
kubectl logs -l app.kubernetes.io/component=backend -n todo-app --tail=20

# View frontend logs
kubectl logs -l app.kubernetes.io/component=frontend -n todo-app --tail=20
```

**Explanation:**
- `-l app.kubernetes.io/component=backend`: Select pods by label
- `--tail=20`: Show last 20 lines of logs
- Useful for debugging if pods aren't working

**Expected backend logs:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 8.6 Describe Pod (if issues)

```powershell
# Get detailed information about a pod
kubectl describe pod <pod-name> -n todo-app
```

**Explanation:**
- Shows events, environment variables, resource limits, etc.
- Use this if a pod is not starting or crashing

**Example:**
```powershell
kubectl describe pod todo-chatbot-backend-67446bd7dd-fgdqj -n todo-app
```

---

## Step 9: Access the Application

**What we're doing:** Set up port forwarding to access services from your local machine.

### 9.1 Port Forward Backend

```powershell
# Forward backend service to localhost:8000
kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app
```

**Explanation:**
- `kubectl port-forward`: Creates a tunnel from your localhost to a Kubernetes service
- `svc/todo-chatbot-backend`: The service to forward
- `8000:8000`: Map local port 8000 to service port 8000
- This runs in the foreground (keep terminal open)

**Expected output:**
```
Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000
```

### 9.2 Port Forward Frontend (in new terminal)

Open a **new PowerShell terminal** and run:

```powershell
# Forward frontend service to localhost:3000
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app
```

**Explanation:**
- Same concept as backend, but for frontend service
- Port 3000 is the standard Next.js development port

### 9.3 Access in Browser

Now you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API Documentation**: http://localhost:8000/docs
- **Backend ReDoc**: http://localhost:8000/redoc
- **Backend Health Check**: http://localhost:8000/health

**Alternative: Run Port Forwarding in Background (PowerShell)**

```powershell
# Start backend port forwarding in background
Start-Job -ScriptBlock { kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app }

# Start frontend port forwarding in background
Start-Job -ScriptBlock { kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app }

# Check background jobs
Get-Job

# View job output
Receive-Job -Id <job-id>
```

**Explanation:**
- `Start-Job`: Runs command in background
- Allows you to continue using the terminal
- Jobs run until you stop them or close the terminal

---

## Step 10: Troubleshooting

### 10.1 Pods Not Starting

**Check pod status:**
```powershell
kubectl get pods -n todo-app
```

**Check pod events:**
```powershell
kubectl describe pod <pod-name> -n todo-app
```

**Check pod logs:**
```powershell
kubectl logs <pod-name> -n todo-app
```

**Common issues:**
- **ImagePullBackOff**: Image not found in Minikube → Run `minikube image load`
- **CrashLoopBackOff**: Application error → Check logs
- **CreateContainerConfigError**: Missing secrets → Verify secrets exist

### 10.2 Services Not Accessible

**Check service endpoints:**
```powershell
kubectl get endpoints -n todo-app
```

**Test from within cluster:**
```powershell
# Run a test pod
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl http://todo-chatbot-backend:8000/health
```

**Explanation:**
- Creates a temporary pod with curl
- Tests connectivity to backend service
- Pod is automatically deleted when done

### 10.3 Update Secrets

If you need to update secrets:

```powershell
# Delete old secret
kubectl delete secret todo-secrets -n todo-app

# Create new secret (with updated values)
kubectl create secret generic todo-secrets `
  --from-literal=DATABASE_URL="new-value" `
  --from-literal=SECRET_KEY="new-value" `
  --from-literal=OPENAI_API_KEY="new-value" `
  -n todo-app

# Restart deployment to pick up new secret
kubectl rollout restart deployment/todo-chatbot-backend -n todo-app
```

### 10.4 View Resource Usage

```powershell
# Check resource usage of pods
kubectl top pods -n todo-app

# Check node resource usage
kubectl top node
```

**Note:** Requires metrics-server addon (we enabled it in Step 2.3)

### 10.5 Restart Deployments

```powershell
# Restart backend deployment
kubectl rollout restart deployment/todo-chatbot-backend -n todo-app

# Restart frontend deployment
kubectl rollout restart deployment/todo-chatbot-frontend -n todo-app

# Check rollout status
kubectl rollout status deployment/todo-chatbot-backend -n todo-app
```

---

## Cleanup Commands

### Remove Helm Release

```powershell
# Uninstall the Helm release
helm uninstall todo-chatbot -n todo-app
```

**Explanation:**
- Removes all resources created by Helm
- Deletes deployments, services, configmaps, etc.

### Delete Namespace

```powershell
# Delete namespace (removes all resources in it)
kubectl delete namespace todo-app
```

**Explanation:**
- Deletes the entire namespace and all resources
- Use with caution!

### Stop Minikube

```powershell
# Stop Minikube (keeps cluster data)
minikube stop

# Delete Minikube cluster (removes everything)
minikube delete
```

**Explanation:**
- `minikube stop`: Stops the cluster but keeps data (can restart later)
- `minikube delete`: Completely removes the cluster

### Remove Docker Images

```powershell
# Remove images from Docker Desktop
docker rmi todo-backend:latest todo-frontend:latest

# Remove images from Minikube
minikube image rm todo-backend:latest
minikube image rm todo-frontend:latest
```

---

## Quick Reference: All Commands in Order

Here's a quick reference of all commands in sequence:

```powershell
# 1. Verify installations
docker --version
minikube version
kubectl version --client
helm version

# 2. Start Minikube
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
minikube addons enable metrics-server

# 3. Build images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# 4. Load images into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# 5. Create namespace
kubectl create namespace todo-app

# 6. Create secrets (extract from .env first)
$envContent = Get-Content backend\.env -Raw
# ... extract values (see Step 6.2) ...
kubectl create secret generic todo-secrets `
  --from-literal=DATABASE_URL="$dbUrl" `
  --from-literal=SECRET_KEY="$secretKey" `
  --from-literal=OPENAI_API_KEY="$openaiKey" `
  -n todo-app

# 7. Deploy with Helm
cd helm\todo-chatbot
helm lint .
helm install todo-chatbot . -n todo-app --create-namespace

# 8. Verify
kubectl get pods -n todo-app
kubectl get svc -n todo-app
kubectl get all -n todo-app

# 9. Access application
kubectl port-forward svc/todo-chatbot-backend 8000:8000 -n todo-app
# (In new terminal)
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app
```

---

## Using AI Tools (Optional)

### kubectl-ai Examples

```powershell
# Check cluster health
kubectl-ai "check the health of all pods in todo-app namespace"

# Scale deployment
kubectl-ai "scale todo-chatbot-backend to 3 replicas in todo-app namespace"

# Troubleshoot issues
kubectl-ai "why are pods failing in todo-app namespace?"

# Get resource usage
kubectl-ai "show me the resource usage of all pods in todo-app namespace"
```

### kagent Examples

```powershell
# Analyze cluster health
kagent "analyze the health of the todo-app namespace"

# Optimize resources
kagent "optimize resource allocation for the todo-chatbot deployment"
```

---

## Summary

This guide walked you through:

1. ✅ Setting up Minikube Kubernetes cluster
2. ✅ Building Docker images for frontend and backend
3. ✅ Loading images into Minikube
4. ✅ Creating Kubernetes secrets for sensitive data
5. ✅ Deploying application using Helm charts
6. ✅ Verifying deployment status
7. ✅ Accessing application via port forwarding

Your Todo Chatbot is now running on Kubernetes! 🎉

---

## Next Steps

- **Production Deployment**: Use a managed Kubernetes service (EKS, GKE, AKS)
- **CI/CD**: Automate builds and deployments
- **Monitoring**: Set up Prometheus and Grafana
- **Scaling**: Configure Horizontal Pod Autoscaler (HPA)
- **Service Mesh**: Implement Istio or Linkerd for advanced networking

---

## Additional Resources

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

