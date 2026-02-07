# PowerShell script for Oracle Cloud OKE setup
# Usage: .\scripts\setup-oke.ps1

param(
    [string]$ClusterOCID = $env:CLUSTER_OCID,
    [string]$OCIRegion = $env:OCI_REGION,
    [string]$Namespace = "todo-app"
)

if (-not $ClusterOCID) {
    Write-Host "Error: CLUSTER_OCID not set" -ForegroundColor Red
    Write-Host "Set it as: `$env:CLUSTER_OCID = 'ocid1.cluster...'" -ForegroundColor Yellow
    Write-Host "Or pass as parameter: .\scripts\setup-oke.ps1 -ClusterOCID 'ocid1.cluster...'" -ForegroundColor Yellow
    exit 1
}

if (-not $OCIRegion) {
    $OCIRegion = "us-ashburn-1"
    Write-Host "Using default region: $OCIRegion" -ForegroundColor Yellow
}

Write-Host "Setting up Oracle Cloud OKE deployment..." -ForegroundColor Cyan

# Check prerequisites
$requiredCommands = @("kubectl", "helm", "dapr", "oci")
foreach ($cmd in $requiredCommands) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "Error: $cmd is required but not installed" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Configuring kubectl for OKE cluster..." -ForegroundColor Yellow
oci ce cluster create-kubeconfig `
    --cluster-id $ClusterOCID `
    --file "$HOME\.kube\config" `
    --region $OCIRegion `
    --token-version 2.0.0

Write-Host "Verifying cluster connection..." -ForegroundColor Yellow
kubectl get nodes

Write-Host "Installing Dapr on OKE..." -ForegroundColor Yellow
dapr init -k

Write-Host "Waiting for Dapr to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s

Write-Host "Creating namespace..." -ForegroundColor Yellow
kubectl create namespace $Namespace --dry-run=client -o yaml | kubectl apply -f -

Write-Host "Applying Dapr components..." -ForegroundColor Yellow
kubectl apply -f dapr/components/
kubectl apply -f dapr/configurations/

Write-Host "Verifying Dapr installation..." -ForegroundColor Yellow
kubectl get pods -n dapr-system
kubectl get components -n default

Write-Host ""
Write-Host "✅ OKE setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create secrets: kubectl create secret generic todo-secrets ... -n $Namespace" -ForegroundColor White
Write-Host "2. Update Helm values with your image registry" -ForegroundColor White
Write-Host "3. Deploy: helm install todo-chatbot helm/todo-chatbot -n $Namespace" -ForegroundColor White

