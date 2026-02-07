# Script to help get cluster information and configure kubectl
# Usage: .\scripts\get-cluster-info.ps1

Write-Host "Getting OKE cluster information..." -ForegroundColor Cyan

# Check if OCI CLI is installed
if (-not (Get-Command oci -ErrorAction SilentlyContinue)) {
    Write-Host "❌ OCI CLI is not installed" -ForegroundColor Red
    Write-Host "Install from: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm" -ForegroundColor Yellow
    exit 1
}

# List clusters
Write-Host "`nFetching clusters in your tenancy..." -ForegroundColor Yellow
$clusters = oci ce cluster list --all --query "data.items[*].{name:name, id:id, state:lifecycle-state, region:\"region\"}" --output json | ConvertFrom-Json

if ($clusters.Count -eq 0) {
    Write-Host "No clusters found. Make sure you're logged in to OCI CLI." -ForegroundColor Red
    exit 1
}

Write-Host "`nFound $($clusters.Count) cluster(s):" -ForegroundColor Green
Write-Host ""

for ($i = 0; $i -lt $clusters.Count; $i++) {
    $cluster = $clusters[$i]
    Write-Host "[$($i + 1)] $($cluster.name)" -ForegroundColor Cyan
    Write-Host "    OCID: $($cluster.id)" -ForegroundColor Gray
    Write-Host "    State: $($cluster.state)" -ForegroundColor $(if ($cluster.state -eq "ACTIVE") { "Green" } else { "Yellow" })
    Write-Host "    Region: $($cluster.region)" -ForegroundColor Gray
    Write-Host ""
}

if ($clusters.Count -eq 1) {
    $selectedCluster = $clusters[0]
    Write-Host "Using the only cluster: $($selectedCluster.name)" -ForegroundColor Green
} else {
    $selection = Read-Host "Select cluster number (1-$($clusters.Count))"
    $selectedCluster = $clusters[[int]$selection - 1]
}

Write-Host "`nSelected: $($selectedCluster.name)" -ForegroundColor Green
Write-Host "OCID: $($selectedCluster.id)" -ForegroundColor Yellow
Write-Host "Region: $($selectedCluster.region)" -ForegroundColor Yellow

# Configure kubectl
Write-Host "`nConfiguring kubectl..." -ForegroundColor Cyan
oci ce cluster create-kubeconfig `
    --cluster-id $selectedCluster.id `
    --file "$HOME\.kube\config" `
    --region $selectedCluster.region `
    --token-version 2.0.0

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ kubectl configured successfully!" -ForegroundColor Green
    
    # Test connection
    Write-Host "`nTesting connection..." -ForegroundColor Yellow
    kubectl get nodes
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Successfully connected to cluster!" -ForegroundColor Green
        Write-Host "`nNext steps:" -ForegroundColor Cyan
        Write-Host "  1. Install Dapr: dapr init -k" -ForegroundColor White
        Write-Host "  2. Apply Dapr components: kubectl apply -f dapr/components/" -ForegroundColor White
        Write-Host "  3. Deploy application: helm install todo-chatbot helm/todo-chatbot -n todo-app" -ForegroundColor White
    }
} else {
    Write-Host "❌ Failed to configure kubectl" -ForegroundColor Red
}

