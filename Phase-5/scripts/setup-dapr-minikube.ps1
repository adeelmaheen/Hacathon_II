# PowerShell script for setting up Dapr on Minikube
# Usage: .\scripts\setup-dapr-minikube.ps1

Write-Host "Setting up Dapr on Minikube..." -ForegroundColor Cyan

# Check if Dapr CLI is installed
if (-not (Get-Command dapr -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Dapr CLI is not installed" -ForegroundColor Red
    Write-Host "Install from: https://docs.dapr.io/getting-started/install-dapr-cli/" -ForegroundColor Yellow
    exit 1
}

# Check if Minikube is running
$minikubeStatus = minikube status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Minikube is not running" -ForegroundColor Red
    Write-Host "Start Minikube first: minikube start" -ForegroundColor Yellow
    exit 1
}

# Initialize Dapr on Kubernetes
Write-Host "Initializing Dapr on Kubernetes..." -ForegroundColor Yellow
dapr init -k

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to initialize Dapr" -ForegroundColor Red
    exit 1
}

# Wait for Dapr to be ready
Write-Host "Waiting for Dapr to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s

# Apply Dapr components
Write-Host "Applying Dapr components..." -ForegroundColor Yellow
kubectl apply -f dapr/components/

# Verify Dapr installation
Write-Host ""
Write-Host "✓ Dapr installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Dapr system pods:" -ForegroundColor Cyan
kubectl get pods -n dapr-system

Write-Host ""
Write-Host "Dapr components:" -ForegroundColor Cyan
kubectl get components -n default

Write-Host ""
Write-Host "To use Dapr in your application, add annotations to your deployment:" -ForegroundColor Yellow
Write-Host "  annotations:" -ForegroundColor White
Write-Host "    dapr.io/enabled: `"true`"" -ForegroundColor White
Write-Host "    dapr.io/app-id: `"todo-backend`"" -ForegroundColor White
Write-Host "    dapr.io/app-port: `"8000`"" -ForegroundColor White

