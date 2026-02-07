# Simple deployment script - does everything automatically
# Just provide cluster OCID when prompted

param(
    [string]$ClusterOCID,
    [string]$Region = "us-ashburn-1"
)

Write-Host "`n=== AUTOMATED DEPLOYMENT TO OKE ===" -ForegroundColor Green

# Check if we need cluster OCID
if (-not $ClusterOCID) {
    Write-Host "`nTo deploy to OKE, I need your cluster OCID." -ForegroundColor Yellow
    Write-Host "Get it from: OCI Console → OKE → Your Cluster → Cluster Information" -ForegroundColor Cyan
    Write-Host ""
    $ClusterOCID = Read-Host "Enter Cluster OCID (or press Enter to use OCI Console 'Access Cluster' command)"
    
    if (-not $ClusterOCID) {
        Write-Host "`nAlternative: Use OCI Console's 'Access Cluster' feature:" -ForegroundColor Yellow
        Write-Host "1. Go to OCI Console → OKE → Your Cluster" -ForegroundColor White
        Write-Host "2. Click 'Access Cluster'" -ForegroundColor White
        Write-Host "3. Copy the command and run it in a new terminal" -ForegroundColor White
        Write-Host "4. Then come back and run this script again" -ForegroundColor White
        exit 0
    }
}

# Check if kubectl is pointing to OKE
Write-Host "`nChecking kubectl context..." -ForegroundColor Cyan
$currentContext = kubectl config current-context 2>&1
$nodesOutput = kubectl get nodes 2>&1 | Out-String

if ($nodesOutput -match "minikube") {
    Write-Host "⚠ kubectl is currently pointing to Minikube" -ForegroundColor Yellow
    Write-Host "Configuring for OKE cluster..." -ForegroundColor Cyan
    
    # Try to configure using OCI CLI if available
    if (Get-Command oci -ErrorAction SilentlyContinue) {
        oci ce cluster create-kubeconfig `
            --cluster-id $ClusterOCID `
            --file "$HOME\.kube\config" `
            --region $Region `
            --token-version 2.0.0
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ kubectl configured for OKE" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to configure kubectl" -ForegroundColor Red
            Write-Host "Please configure manually using OCI Console 'Access Cluster' command" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "❌ OCI CLI not installed" -ForegroundColor Red
        Write-Host "Please:" -ForegroundColor Yellow
        Write-Host "  1. Install OCI CLI, OR" -ForegroundColor White
        Write-Host "  2. Use OCI Console 'Access Cluster' to configure kubectl" -ForegroundColor White
        exit 1
    }
} else {
    Write-Host "✓ kubectl appears to be configured" -ForegroundColor Green
}

# Verify connection
Write-Host "`nVerifying cluster connection..." -ForegroundColor Cyan
kubectl get nodes
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Cannot connect to cluster" -ForegroundColor Red
    exit 1
}

# Install Dapr if not installed
Write-Host "`nChecking Dapr installation..." -ForegroundColor Cyan
kubectl get pods -n dapr-system 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing Dapr..." -ForegroundColor Yellow
    dapr init -k
    Write-Host "Waiting for Dapr to be ready..." -ForegroundColor Yellow
    kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s
} else {
    Write-Host "✓ Dapr already installed" -ForegroundColor Green
}

# Create namespace and apply Dapr components
Write-Host "`nSetting up Dapr components..." -ForegroundColor Cyan
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f dapr/components/ 2>&1 | Out-Null
kubectl apply -f dapr/configurations/ 2>&1 | Out-Null
Write-Host "✓ Dapr components applied" -ForegroundColor Green

# Check if images exist
Write-Host "`nChecking Docker images..." -ForegroundColor Cyan
$backendImage = docker images todo-backend:latest -q
$frontendImage = docker images todo-frontend:latest -q

if (-not $backendImage) {
    Write-Host "Building backend image..." -ForegroundColor Yellow
    docker build -t todo-backend:latest ./backend
}

if (-not $frontendImage) {
    Write-Host "Building frontend image..." -ForegroundColor Yellow
    docker build -t todo-frontend:latest ./frontend
}

Write-Host "✓ Images ready" -ForegroundColor Green

# Ask about image registry
Write-Host "`nImage Registry Options:" -ForegroundColor Cyan
Write-Host "  1. Docker Hub (requires login)" -ForegroundColor White
Write-Host "  2. OCI Container Registry" -ForegroundColor White
Write-Host "  3. Skip push (use local images - requires image pull secrets)" -ForegroundColor White
$registryChoice = Read-Host "Choose option (1-3)"

$BackendImage = "todo-backend:latest"
$FrontendImage = "todo-frontend:latest"

if ($registryChoice -eq "1") {
    $dockerHubUser = Read-Host "Enter Docker Hub username"
    docker login
    docker tag todo-backend:latest "$dockerHubUser/todo-backend:latest"
    docker tag todo-frontend:latest "$dockerHubUser/todo-frontend:latest"
    docker push "$dockerHubUser/todo-backend:latest"
    docker push "$dockerHubUser/todo-frontend:latest"
    $BackendImage = "$dockerHubUser/todo-backend:latest"
    $FrontendImage = "$dockerHubUser/todo-frontend:latest"
} elseif ($registryChoice -eq "2") {
    $ociRegion = Read-Host "Enter OCI region"
    $tenancy = Read-Host "Enter tenancy namespace"
    $repo = Read-Host "Enter repository name"
    Write-Host "Logging in to OCI Registry..." -ForegroundColor Yellow
    docker login "$ociRegion.ocir.io"
    docker tag todo-backend:latest "$ociRegion.ocir.io/$tenancy/$repo/backend:latest"
    docker tag todo-frontend:latest "$ociRegion.ocir.io/$tenancy/$repo/frontend:latest"
    docker push "$ociRegion.ocir.io/$tenancy/$repo/backend:latest"
    docker push "$ociRegion.ocir.io/$tenancy/$repo/frontend:latest"
    $BackendImage = "$ociRegion.ocir.io/$tenancy/$repo/backend:latest"
    $FrontendImage = "$ociRegion.ocir.io/$tenancy/$repo/frontend:latest"
}

# Create secrets
Write-Host "`nCreating secrets..." -ForegroundColor Cyan
$dbUrl = Read-Host "Enter DATABASE_URL (from Neon PostgreSQL)"
$secretKey = Read-Host "Enter SECRET_KEY (or press Enter to generate)"
if (-not $secretKey) {
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    Write-Host "Generated SECRET_KEY: $secretKey" -ForegroundColor Green
}
$openaiKey = Read-Host "Enter OPENAI_API_KEY"

kubectl create secret generic todo-secrets `
    --from-literal=DATABASE_URL="$dbUrl" `
    --from-literal=SECRET_KEY="$secretKey" `
    --from-literal=OPENAI_API_KEY="$openaiKey" `
    -n todo-app `
    --dry-run=client -o yaml | kubectl apply -f -

Write-Host "✓ Secrets created" -ForegroundColor Green

# Update Helm values
Write-Host "`nUpdating Helm values..." -ForegroundColor Cyan
$valuesFile = "helm/todo-chatbot/values.yaml"
$values = Get-Content $valuesFile -Raw
$values = $values -replace "(repository: )todo-backend", "`$1$BackendImage"
$values = $values -replace "(repository: )todo-frontend", "`$1$FrontendImage"
Set-Content $valuesFile $values

# Deploy
Write-Host "`nDeploying application..." -ForegroundColor Cyan
cd helm/todo-chatbot
helm upgrade --install todo-chatbot . -n todo-app --create-namespace

Write-Host "`nWaiting for pods..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
kubectl get pods -n todo-app

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "`nTo access:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app" -ForegroundColor White
Write-Host "  Then open: http://localhost:3000" -ForegroundColor White

cd ../..

