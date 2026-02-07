# PowerShell script for building Docker images on Windows
# Usage: .\scripts\build-images.ps1 [backend|frontend|all]

param(
    [Parameter(Position=0)]
    [ValidateSet("backend", "frontend", "all")]
    [string]$Target = "all"
)

$BackendImage = "todo-backend:latest"
$FrontendImage = "todo-frontend:latest"

function Build-Backend {
    Write-Host "Building backend image..." -ForegroundColor Cyan
    Set-Location backend
    docker build -t $BackendImage .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Backend image built: $BackendImage" -ForegroundColor Green
    } else {
        Write-Host "✗ Backend build failed" -ForegroundColor Red
        exit 1
    }
    Set-Location ..
}

function Build-Frontend {
    Write-Host "Building frontend image..." -ForegroundColor Cyan
    Set-Location frontend
    docker build -t $FrontendImage .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Frontend image built: $FrontendImage" -ForegroundColor Green
    } else {
        Write-Host "✗ Frontend build failed" -ForegroundColor Red
        exit 1
    }
    Set-Location ..
}

function Load-ToMinikube {
    if (Get-Command minikube -ErrorAction SilentlyContinue) {
        Write-Host "Loading images to Minikube..." -ForegroundColor Cyan
        minikube image load $BackendImage
        minikube image load $FrontendImage
        Write-Host "✓ Images loaded to Minikube" -ForegroundColor Green
    } else {
        Write-Host "Minikube not found, skipping image load" -ForegroundColor Yellow
    }
}

switch ($Target) {
    "backend" {
        Build-Backend
    }
    "frontend" {
        Build-Frontend
    }
    "all" {
        Build-Backend
        Build-Frontend
        Load-ToMinikube
    }
}

Write-Host "Build complete!" -ForegroundColor Green

