#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Deploy frontend to Azure Static Web Apps using SWA CLI

.DESCRIPTION
    This script builds the React frontend and deploys it to Azure Static Web Apps
    using the SWA CLI for direct deployment (bypassing GitHub integration).

.PARAMETER Environment
    The deployment environment (default: production)

.EXAMPLE
    .\deploy-frontend-swa.ps1
    
.EXAMPLE
    .\deploy-frontend-swa.ps1 -Environment staging
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$Environment = "production",
    [Parameter(Mandatory = $false)]
    [string]$DeploymentToken
)

# Set error action preference
$ErrorActionPreference = "Stop"


Write-Host "🚀 Starting frontend deployment to Azure Static Web Apps..." -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Cyan
if ($DeploymentToken) {
    Write-Host "Using deployment token from parameter." -ForegroundColor Cyan
} elseif ($env:SWA_DEPLOYMENT_TOKEN) {
    Write-Host "Using deployment token from environment variable SWA_DEPLOYMENT_TOKEN." -ForegroundColor Cyan
    $DeploymentToken = $env:SWA_DEPLOYMENT_TOKEN
} else {
    Write-Host "❗ No deployment token provided. Please provide -DeploymentToken or set SWA_DEPLOYMENT_TOKEN environment variable." -ForegroundColor Red
    exit 1
}

try {
    # Navigate to frontend directory
    Write-Host "📁 Navigating to frontend directory..." -ForegroundColor Yellow
    Push-Location "frontend"
    
    # Install dependencies
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
    
    # Build the project
    Write-Host "🔨 Building React application..." -ForegroundColor Yellow
    npm run build
    
    # Check if build directory exists
    if (-not (Test-Path "build")) {
        throw "Build directory not found. Build may have failed."
    }
    
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    
    # Deploy using SWA CLI
    Write-Host "🌐 Deploying to Azure Static Web Apps..." -ForegroundColor Yellow
    
    if ($Environment -eq "production") {
        swa deploy ./build --env production --deployment-token $DeploymentToken
    } else {
        swa deploy ./build --env $Environment --deployment-token $DeploymentToken
    }
    
    Write-Host "✅ Frontend deployment completed successfully!" -ForegroundColor Green
    Write-Host "🎉 Your changes should now be live on Azure Static Web Apps!" -ForegroundColor Magenta
    
} catch {
    Write-Host "❌ Deployment failed: $_" -ForegroundColor Red
    exit 1
} finally {
    # Return to original directory
    Pop-Location
}

Write-Host ""
Write-Host "💡 Tip: If changes don't appear immediately, try:" -ForegroundColor Cyan
Write-Host "   - Hard refresh the browser (Ctrl+F5)" -ForegroundColor Gray
Write-Host "   - Clear browser cache" -ForegroundColor Gray
Write-Host "   - Wait a few minutes for CDN propagation" -ForegroundColor Gray
Write-Host ""
Write-Host "🔑 To get your deployment token:" -ForegroundColor Yellow
Write-Host "   1. Go to your Static Web App in the Azure Portal." -ForegroundColor Gray
Write-Host "   2. Click 'Deployment Token' in the left menu." -ForegroundColor Gray
Write-Host "   3. Click 'Show' and copy the token." -ForegroundColor Gray
Write-Host "   4. Pass it to this script with -DeploymentToken or set SWA_DEPLOYMENT_TOKEN env variable." -ForegroundColor Gray
