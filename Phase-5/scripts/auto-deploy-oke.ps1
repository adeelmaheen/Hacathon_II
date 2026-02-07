# Automated deployment script for OKE
# This script will do everything automatically

param(
    [string]$ClusterOCID = $env:CLUSTER_OCID,
    [string]$OCIRegion = $env:OCI_REGION,
    [string]$DockerHubUsername = $env:DOCKERHUB_USERNAME,
    [string]$ImageRegistry = "docker.io"  # or "ocir.io"
)

$ErrorActionPreference = "Stop"

Write-Host "`n=== AUTOMATED OKE DEPLOYMENT ===" -ForegroundColor Green
Write-Host "This script will:" -ForegroundColor Cyan
Write-Host "  1. Configure kubectl" -ForegroundColor White
Write-Host "  2. Install Dapr" -ForegroundColor White
Write-Host "  3. Build Docker images" -ForegroundColor White
Write-Host "  4. Push images to registry" -ForegroundColor White
Write-Host "  5. Deploy application" -ForegroundColor White
Write-Host ""

# Step 1: Configure kubectl
if (-not $ClusterOCID) {
    Write-Host "Step 1: Getting cluster OCID..." -ForegroundColor Yellow
    if (Get-Command oci -ErrorAction SilentlyContinue) {
        $clusters = oci ce cluster list --all --query "data.items[*].{name:name, id:id, state:lifecycle-state, region:\"region\"}" --output json 2>&1
        if ($LASTEXITCODE -eq 0 -and $clusters) {
            $clusterData = $clusters | ConvertFrom-Json
            if ($clusterData.Count -eq 1) {
                $ClusterOCID = $clusterData[0].id
                $OCIRegion = $clusterData[0].region
                Write-Host "✓ Found cluster: $($clusterData[0].name)" -ForegroundColor Green
            } elseif ($clusterData.Count -gt 1) {
                Write-Host "Multiple clusters found:" -ForegroundColor Yellow
                for ($i = 0; $i -lt $clusterData.Count; $i++) {
                    Write-Host "  [$($i+1)] $($clusterData[$i].name) - $($clusterData[$i].state)" -ForegroundColor White
                }
                $selection = Read-Host "Select cluster number"
                $selected = $clusterData[[int]$selection - 1]
                $ClusterOCID = $selected.id
                $OCIRegion = $selected.region
            }
        }
    }
    
    if (-not $ClusterOCID) {
        Write-Host "❌ Could not get cluster OCID automatically" -ForegroundColor Red
        Write-Host "Please provide: .\scripts\auto-deploy-oke.ps1 -ClusterOCID 'ocid1...' -OCIRegion 'us-ashburn-1'" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "`nStep 1: Configuring kubectl..." -ForegroundColor Cyan
oci ce cluster create-kubeconfig `
    --cluster-id $ClusterOCID `
    --file "$HOME\.kube\config" `
    --region $OCIRegion `
    --token-version 2.0.0

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to configure kubectl" -ForegroundColor Red
    exit 1
}

Write-Host "✓ kubectl configured" -ForegroundColor Green
kubectl get nodes

# Step 2: Install Dapr
Write-Host "`nStep 2: Installing Dapr..." -ForegroundColor Cyan
kubectl get pods -n dapr-system 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    dapr init -k
    kubectl wait --for=condition=Ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s
} else {
    Write-Host "✓ Dapr already installed" -ForegroundColor Green
}

# Step 3: Create namespace and apply Dapr components
Write-Host "`nStep 3: Setting up Dapr components..." -ForegroundColor Cyan
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f dapr/components/
kubectl apply -f dapr/configurations/

# Step 4: Build images if needed
Write-Host "`nStep 4: Building Docker images..." -ForegroundColor Cyan
if (-not (docker images todo-backend:latest -q)) {
    Write-Host "Building backend..." -ForegroundColor Yellow
    docker build -t todo-backend:latest ./backend
} else {
    Write-Host "✓ Backend image exists" -ForegroundColor Green
}

if (-not (docker images todo-frontend:latest -q)) {
    Write-Host "Building frontend..." -ForegroundColor Yellow
    docker build -t todo-frontend:latest ./frontend
} else {
    Write-Host "✓ Frontend image exists" -ForegroundColor Green
}

# Step 5: Push images
if ($DockerHubUsername) {
    Write-Host "`nStep 5: Pushing images to Docker Hub..." -ForegroundColor Cyan
    docker tag todo-backend:latest "$DockerHubUsername/todo-backend:latest"
    docker tag todo-frontend:latest "$DockerHubUsername/todo-frontend:latest"
    
    docker push "$DockerHubUsername/todo-backend:latest"
    docker push "$DockerHubUsername/todo-frontend:latest"
    
    $BackendImage = "$DockerHubUsername/todo-backend:latest"
    $FrontendImage = "$DockerHubUsername/todo-frontend:latest"
} else {
    Write-Host "`nStep 5: Skipping image push (no DockerHub username provided)" -ForegroundColor Yellow
    Write-Host "Images need to be pushed manually or loaded into cluster" -ForegroundColor Yellow
    $BackendImage = "todo-backend:latest"
    $FrontendImage = "todo-frontend:latest"
}

# Step 6: Create secrets (will need user input)
Write-Host "`nStep 6: Creating secrets..." -ForegroundColor Cyan
Write-Host "You need to provide:" -ForegroundColor Yellow
Write-Host "  - DATABASE_URL (from Neon PostgreSQL)" -ForegroundColor White
Write-Host "  - SECRET_KEY (generate a random string)" -ForegroundColor White
Write-Host "  - OPENAI_API_KEY (from OpenAI)" -ForegroundColor White
Write-Host ""
$dbUrl = Read-Host "Enter DATABASE_URL"
$secretKey = Read-Host "Enter SECRET_KEY"
$openaiKey = Read-Host "Enter OPENAI_API_KEY"

kubectl create secret generic todo-secrets `
    --from-literal=DATABASE_URL="$dbUrl" `
    --from-literal=SECRET_KEY="$secretKey" `
    --from-literal=OPENAI_API_KEY="$openaiKey" `
    -n todo-app `
    --dry-run=client -o yaml | kubectl apply -f -

# Step 7: Update Helm values
Write-Host "`nStep 7: Updating Helm values..." -ForegroundColor Cyan
$valuesFile = "helm/todo-chatbot/values.yaml"
$values = Get-Content $valuesFile -Raw
$values = $values -replace "repository: todo-backend", "repository: $BackendImage"
$values = $values -replace "repository: todo-frontend", "repository: $FrontendImage"
Set-Content $valuesFile $values

# Step 8: Deploy with Helm
Write-Host "`nStep 8: Deploying application..." -ForegroundColor Cyan
cd helm/todo-chatbot
helm upgrade --install todo-chatbot . -n todo-app --create-namespace

# Step 9: Wait for deployment
Write-Host "`nStep 9: Waiting for pods to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 10
kubectl get pods -n todo-app -w

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "`nTo access the application:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app" -ForegroundColor White
Write-Host "  Then open: http://localhost:3000" -ForegroundColor White

cd ../..

