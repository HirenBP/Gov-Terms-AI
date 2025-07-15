# ============================================================================
# Quick Backend Update Script
# ============================================================================

param(
    [string]$ResourceGroup = "RAGdb",
    [string]$ACRName = "cr32p4pozukxrfi",
    [string]$BackendAppName = "cabackend-32p4pozukxrfi"
)

Write-Host "🔄 Quick backend update for Gov Terms AI..." -ForegroundColor Green

try {
    # Check if we're in the right directory
    if (-not (Test-Path "./backend/app.py")) {
        throw "Please run this script from the Gov Terms AI root directory"
    }

    # Step 1: Clean local Docker environment first
    Write-Host "🧹 Cleaning local Docker environment..." -ForegroundColor Yellow
    docker system prune -f
    docker builder prune -f
    
    # Step 2: Build Backend (force fresh build, no cache, no layer reuse)
    Write-Host "📦 Building backend with completely fresh build (no cache, no layers)..." -ForegroundColor Yellow
    docker build --no-cache --pull --force-rm -t gov-terms-backend:latest ./backend
    if ($LASTEXITCODE -ne 0) { throw "Docker build failed" }

    # Step 3: Tag for ACR with timestamp to ensure uniqueness
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $randomSuffix = Get-Random -Minimum 1000 -Maximum 9999
    $uniqueTag = "$timestamp-$randomSuffix"
    Write-Host "🏷️  Tagging for ACR with unique tag: $uniqueTag..." -ForegroundColor Yellow
    docker tag gov-terms-backend:latest ${ACRName}.azurecr.io/gov-terms-backend:$uniqueTag
    docker tag gov-terms-backend:latest ${ACRName}.azurecr.io/gov-terms-backend:latest

    # Step 4: Login to ACR
    Write-Host "🔐 Logging into ACR..." -ForegroundColor Yellow
    az acr login --name $ACRName
    if ($LASTEXITCODE -ne 0) { throw "ACR login failed" }

    # Step 5: Push unique image first (this forces new layers)
    Write-Host "⬆️  Pushing unique timestamped image to ACR (forces new layers)..." -ForegroundColor Yellow
    docker push ${ACRName}.azurecr.io/gov-terms-backend:$uniqueTag
    if ($LASTEXITCODE -ne 0) { throw "Unique image push failed" }
    
    Write-Host "⬆️  Pushing latest tag..." -ForegroundColor Yellow
    docker push ${ACRName}.azurecr.io/gov-terms-backend:latest
    if ($LASTEXITCODE -ne 0) { throw "Latest image push failed" }

    # Step 6: Update Container App with unique timestamped image
    Write-Host "🚀 Updating Container App with completely fresh image: $uniqueTag..." -ForegroundColor Yellow
    az containerapp update `
        --name $BackendAppName `
        --resource-group $ResourceGroup `
        --image ${ACRName}.azurecr.io/gov-terms-backend:$uniqueTag

    if ($LASTEXITCODE -ne 0) { throw "Container app update failed" }

    # Get backend URL
    $backendUrl = az containerapp show --name $BackendAppName --resource-group $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv

    Write-Host "✅ Backend update completed with completely fresh build!" -ForegroundColor Green
    Write-Host "🏷️  Deployed image: ${ACRName}.azurecr.io/gov-terms-backend:$uniqueTag" -ForegroundColor Gray
    Write-Host "🔗 Backend URL: https://$backendUrl" -ForegroundColor Blue
    Write-Host "🔗 Test health: https://$backendUrl/health" -ForegroundColor Cyan
    
    # Clean up old local images to save space
    Write-Host "🧹 Final cleanup of local Docker images..." -ForegroundColor Gray
    docker image prune -a -f

} catch {
    Write-Error "❌ Update failed: $_"
    exit 1
}
