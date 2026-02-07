# PowerShell script for setting up Minikube on Windows
# Usage: .\scripts\setup-minikube.ps1

Write-Host "Setting up Minikube cluster..." -ForegroundColor Cyan

# Check if Minikube is installed
if (-not (Get-Command minikube -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Minikube is not installed" -ForegroundColor Red
    Write-Host "Install from: https://minikube.sigs.k8s.io/docs/start/" -ForegroundColor Yellow
    exit 1
}

# Check if Minikube is already running
$status = minikube status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Minikube is already running" -ForegroundColor Yellow
    $response = Read-Host "Do you want to restart it? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "Stopping Minikube..." -ForegroundColor Cyan
        minikube stop
        minikube delete
    } else {
        Write-Host "Using existing Minikube cluster" -ForegroundColor Green
        exit 0
    }
}

# Start Minikube
Write-Host "Starting Minikube cluster..." -ForegroundColor Cyan
minikube start --driver=docker --memory=4096 --cpus=2

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start Minikube" -ForegroundColor Red
    exit 1
}

# Enable addons
Write-Host "Enabling required addons..." -ForegroundColor Cyan
minikube addons enable ingress
minikube addons enable metrics-server

# Verify addons
Write-Host "Verifying addons..." -ForegroundColor Cyan
minikube addons list

# Get cluster info
Write-Host ""
Write-Host "✓ Minikube cluster is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Cluster info:" -ForegroundColor Cyan
kubectl cluster-info

Write-Host ""
Write-Host "Minikube IP:" -ForegroundColor Cyan
minikube ip

Write-Host ""
Write-Host "To use Minikube's Docker daemon:" -ForegroundColor Yellow
Write-Host "  minikube docker-env | Invoke-Expression" -ForegroundColor White

