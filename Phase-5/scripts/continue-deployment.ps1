# Continue deployment after kubectl is configured
# Run this after you've configured kubectl using OCI Console

Write-Host "`n=== CONTINUING DEPLOYMENT ===" -ForegroundColor Green

# Verify kubectl connection
Write-Host "`nVerifying kubectl connection..." -ForegroundColor Cyan
kubectl get nodes
if ($LASTEXITCODE -ne 0) {
    Write-Host "kubectl not configured. Please configure it first using OCI Console 'Access Cluster'." -ForegroundColor Red
    exit 1
}
Write-Host "kubectl connected!" -ForegroundColor Green

# Install Dapr
Write-Host "`nInstalling Dapr..." -ForegroundColor Cyan
kubectl get pods -n dapr-system 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing Dapr..." -ForegroundColor Yellow
    dapr init -k
    Write-Host "Waiting for Dapr..." -ForegroundColor Yellow
    kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s
} else {
    Write-Host "Dapr already installed" -ForegroundColor Green
}

# Setup namespace and components
Write-Host "`nSetting up Dapr components..." -ForegroundColor Cyan
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f dapr/components/
kubectl apply -f dapr/configurations/
Write-Host "Dapr components applied" -ForegroundColor Green

# Check images
Write-Host "`nChecking Docker images..." -ForegroundColor Cyan
$backendExists = docker images todo-backend:latest -q
$frontendExists = docker images todo-frontend:latest -q

if (-not $backendExists) {
    Write-Host "Building backend..." -ForegroundColor Yellow
    docker build -t todo-backend:latest ./backend
} else {
    Write-Host "Backend image exists" -ForegroundColor Green
}

if (-not $frontendExists) {
    Write-Host "Building frontend..." -ForegroundColor Yellow
    docker build -t todo-frontend:latest ./frontend
} else {
    Write-Host "Frontend image exists" -ForegroundColor Green
}

# Registry choice
Write-Host "`nImage Registry Options:" -ForegroundColor Cyan
Write-Host "1. Docker Hub"
Write-Host "2. Skip push (for now)"
$choice = Read-Host "Choice"

$BackendImage = "todo-backend:latest"
$FrontendImage = "todo-frontend:latest"

if ($choice -eq "1") {
    $user = Read-Host "Docker Hub username"
    Write-Host "Logging in to Docker Hub..." -ForegroundColor Yellow
    docker login
    Write-Host "Tagging images..." -ForegroundColor Yellow
    docker tag todo-backend:latest "$user/todo-backend:latest"
    docker tag todo-frontend:latest "$user/todo-frontend:latest"
    Write-Host "Pushing images..." -ForegroundColor Yellow
    docker push "$user/todo-backend:latest"
    docker push "$user/todo-frontend:latest"
    $BackendImage = "$user/todo-backend:latest"
    $FrontendImage = "$user/todo-frontend:latest"
    Write-Host "Images pushed!" -ForegroundColor Green
}

# Secrets
Write-Host "`nCreating secrets..." -ForegroundColor Cyan
$dbUrl = Read-Host "DATABASE_URL"
$secretKey = Read-Host "SECRET_KEY (or Enter to generate)"
if (-not $secretKey) {
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    Write-Host "Generated SECRET_KEY: $secretKey" -ForegroundColor Green
}
$openaiKey = Read-Host "OPENAI_API_KEY"

kubectl create secret generic todo-secrets --from-literal=DATABASE_URL="$dbUrl" --from-literal=SECRET_KEY="$secretKey" --from-literal=OPENAI_API_KEY="$openaiKey" -n todo-app --dry-run=client -o yaml | kubectl apply -f -
Write-Host "Secrets created" -ForegroundColor Green

# Update Helm values
Write-Host "`nUpdating Helm values..." -ForegroundColor Cyan
$values = Get-Content helm/todo-chatbot/values.yaml -Raw
$values = $values -replace "repository: todo-backend", "repository: $BackendImage"
$values = $values -replace "repository: todo-frontend", "repository: $FrontendImage"
Set-Content helm/todo-chatbot/values.yaml $values

# Deploy
Write-Host "`nDeploying application..." -ForegroundColor Cyan
cd helm/todo-chatbot
helm upgrade --install todo-chatbot . -n todo-app --create-namespace

Write-Host "`nWaiting for pods to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 20
kubectl get pods -n todo-app
kubectl get services -n todo-app

Write-Host "`n=== DEPLOYMENT COMPLETE! ===" -ForegroundColor Green
Write-Host "`nTo access the application:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app" -ForegroundColor White
Write-Host "  Then open: http://localhost:3000" -ForegroundColor White
Write-Host "`nOr expose with LoadBalancer:" -ForegroundColor Cyan
Write-Host "  helm upgrade todo-chatbot . -n todo-app --set frontend.service.type=LoadBalancer" -ForegroundColor White
Write-Host "  kubectl get svc todo-chatbot-frontend -n todo-app" -ForegroundColor White

cd ../..

