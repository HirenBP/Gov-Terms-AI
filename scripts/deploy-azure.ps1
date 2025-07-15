# Variables
$ResourceGroup = "RAGdb"
$ACRName = "cr32p4pozukxrfi"
$BackendImageName = "govterms-backend"
$BackendAppName = "cabackend-32p4pozukxrfi"
$tag = "latest"  # or "1407" for date-based tag

# Construct full image name with proper variable delimiting
$acrImageName = "${ACRName}.azurecr.io/${BackendImageName}:${tag}"

# Build Docker image locally with tag
docker build --no-cache --pull --force-rm -t "${BackendImageName}:${tag}" ./backend
if ($LASTEXITCODE -ne 0) { throw "Backend Docker build failed" }

# Tag the image for Azure Container Registry
docker tag "${BackendImageName}:${tag}" "$acrImageName"
if ($LASTEXITCODE -ne 0) { throw "Docker tag failed" }

# Login to Azure Container Registry
az acr login --name $ACRName
if ($LASTEXITCODE -ne 0) { throw "ACR login failed" }

# Push the image to Azure Container Registry
docker push "$acrImageName"
if ($LASTEXITCODE -ne 0) { throw "Docker push failed" }

# Prepare JSON to update container app specifying container name and image
$containerUpdate = @"
[
  {
    "name": "backend",
    "image": "$acrImageName"
  }
]
"@

# Update the Azure Container App with new image
az containerapp update `
    --name $BackendAppName `
    --resource-group $ResourceGroup `
    --containers "$containerUpdate"
if ($LASTEXITCODE -ne 0) { throw "Backend deployment failed" }

Write-Host "✅ Deployment succeeded with image $acrImageName"
