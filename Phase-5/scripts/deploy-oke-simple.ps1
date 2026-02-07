# Simple OKE deployment script
param(
    [string]$ClusterOCID,
    [string]$Region = "us-ashburn-1"
)

Write-Host "`n=== AUTOMATED DEPLOYMENT TO OKE ===" -ForegroundColor Green

# Get cluster OCID
if (-not $ClusterOCID) {
    Write-Host "`nEnter your OKE cluster OCID:" -ForegroundColor Yellow
    Write-Host "Get it from: OCI Console -> OKE -> Your Cluster -> Cluster Information" -ForegroundColor Cyan
    $ClusterOCID = Read-Host "Cluster OCID"
    if (-not $ClusterOCID) {
        Write-Host "Cluster OCID is required. Exiting." -ForegroundColor Red
        exit 1
    }
}

# Configure kubectl
Write-Host "`nConfiguring kubectl..." -ForegroundColor Cyan
if (Get-Command oci -ErrorAction SilentlyContinue) {
    oci ce cluster create-kubeconfig --cluster-id $ClusterOCID --file "$HOME\.kube\config" --region $Region --token-version 2.0.0
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to configure kubectl. Please use OCI Console 'Access Cluster' command." -ForegroundColor Red
        exit 1
    }
    Write-Host "kubectl configured" -ForegroundColor Green
} else {
    Write-Host "OCI CLI not found. Please configure kubectl manually using OCI Console 'Access Cluster'." -ForegroundColor Yellow
    exit 1
}

# Verify connection
Write-Host "`nVerifying connection..." -ForegroundColor Cyan
kubectl get nodes
if ($LASTEXITCODE -ne 0) {
    Write-Host "Cannot connect to cluster" -ForegroundColor Red
    exit 1
}

# Install Dapr
Write-Host "`nInstalling Dapr..." -ForegroundColor Cyan
kubectl get pods -n dapr-system 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    dapr init -k
    kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s
} else {
    Write-Host "Dapr already installed" -ForegroundColor Green
}

# Setup namespace and components
Write-Host "`nSetting up Dapr components..." -ForegroundColor Cyan
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f dapr/components/
kubectl apply -f dapr/configurations/

# Check images
Write-Host "`nChecking images..." -ForegroundColor Cyan
$backendExists = docker images todo-backend:latest -q
$frontendExists = docker images todo-frontend:latest -q

if (-not $backendExists) {
    Write-Host "Building backend..." -ForegroundColor Yellow
    docker build -t todo-backend:latest ./backend
}
if (-not $frontendExists) {
    Write-Host "Building frontend..." -ForegroundColor Yellow
    docker build -t todo-frontend:latest ./frontend
}

# Registry choice
Write-Host "`nImage Registry:" -ForegroundColor Cyan
Write-Host "1. Docker Hub"
Write-Host "2. Skip push (use local)"
$choice = Read-Host "Choice"

$BackendImage = "todo-backend:latest"
$FrontendImage = "todo-frontend:latest"

if ($choice -eq "1") {
    $user = Read-Host "Docker Hub username"
    docker login
    docker tag todo-backend:latest "$user/todo-backend:latest"
    docker tag todo-frontend:latest "$user/todo-frontend:latest"
    docker push "$user/todo-backend:latest"
    docker push "$user/todo-frontend:latest"
    $BackendImage = "$user/todo-backend:latest"
    $FrontendImage = "$user/todo-frontend:latest"
}

# Secrets
Write-Host "`nCreating secrets..." -ForegroundColor Cyan
$dbUrl = Read-Host "DATABASE_URL"
$secretKey = Read-Host "SECRET_KEY (or Enter to generate)"
if (-not $secretKey) {
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    Write-Host "Generated: $secretKey" -ForegroundColor Green
}
$openaiKey = Read-Host "OPENAI_API_KEY"

kubectl create secret generic todo-secrets --from-literal=DATABASE_URL="$dbUrl" --from-literal=SECRET_KEY="$secretKey" --from-literal=OPENAI_API_KEY="$openaiKey" -n todo-app --dry-run=client -o yaml | kubectl apply -f -

# Update Helm values
Write-Host "`nUpdating Helm values..." -ForegroundColor Cyan
$values = Get-Content helm/todo-chatbot/values.yaml -Raw
$values = $values -replace "repository: todo-backend", "repository: $BackendImage"
$values = $values -replace "repository: todo-frontend", "repository: $FrontendImage"
Set-Content helm/todo-chatbot/values.yaml $values

# Deploy
Write-Host "`nDeploying..." -ForegroundColor Cyan
cd helm/todo-chatbot
helm upgrade --install todo-chatbot . -n todo-app --create-namespace

Write-Host "`nWaiting..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
kubectl get pods -n todo-app

Write-Host "`nDeployment complete!" -ForegroundColor Green
Write-Host "`nAccess with: kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app" -ForegroundColor Cyan

cd ../..

