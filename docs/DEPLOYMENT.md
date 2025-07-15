# Deployment Guide - Gov Terms AI

This guide covers the current Azure deployment and maintenance procedures for the Gov Terms AI application.

## 🌐 Current Production Deployment

### Live Application URLs

**Frontend**: https://wonderful-water-00378c20f.2.azurestaticapps.net  
**Backend**: https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io  

### Azure Resources

**Resource Group**: `RAGdb` (East US 2)

- **Static Web App**: `stapp32p4pozukxrfi`
  - Frontend hosting for React application
  - Automatic builds and deployments
  - Custom domain support available

- **Container App**: `cabackend-32p4pozukxrfi`  
  - FastAPI backend in Docker container
  - Auto-scaling enabled (1-10 replicas)
  - Current image: `cr32p4pozukxrfi.azurecr.io/govterms-backend:v2.0.0`

- **Container Registry**: `cr32p4pozukxrfi`
  - Stores Docker images for backend
  - Integrated with Container Apps

- **Key Vault**: `kv32p4pozukxrfi`
  - Stores API keys securely
  - `pinecone-api-key`
  - `google-api-key`

- **Log Analytics**: `log32p4pozukxrfi`
  - Centralized logging for all resources
  - Performance monitoring

## 🚀 Deployment Procedures

### Using Azure Developer CLI (azd)

The project is configured for deployment using Azure Developer CLI:

1. **Install Azure Developer CLI**:
```bash
# Windows (PowerShell)
winget install microsoft.azd

# macOS
brew tap azure/azd && brew install azd

# Linux
curl -fsSL https://aka.ms/install-azd.sh | bash
```

2. **Login to Azure**:
```bash
azd auth login
```

3. **Deploy the application**:
```bash
# Deploy entire application
azd up

# Deploy just the backend
azd deploy backend

# Deploy just the frontend  
azd deploy frontend
```

### Manual Azure CLI Deployment

If you prefer to use Azure CLI directly:

1. **Backend Deployment**:
```bash
# Build and push to registry
az acr build --registry cr32p4pozukxrfi --image govterms-backend:latest ./backend

# Update container app
az containerapp update \
  --name cabackend-32p4pozukxrfi \
  --resource-group RAGdb \
  --image cr32p4pozukxrfi.azurecr.io/govterms-backend:latest
```

2. **Frontend Deployment**:
```bash
# Build frontend
cd frontend && npm run build

# Deploy to static web app
az staticwebapp deploy \
  --name stapp32p4pozukxrfi \
  --resource-group RAGdb \
  --source-location ./build
```

3. **Push to registry**:
```bash
docker push cr32p4pozukxrfi.azurecr.io/govterms-backend:v2.0.0
```

4. **Update Container App**:
```bash
az containerapp update \
  --name cabackend-32p4pozukxrfi \
  --resource-group RAGdb \
  --image cr32p4pozukxrfi.azurecr.io/govterms-backend:v2.0.0
```

5. **Verify deployment**:
```bash
curl https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io/health
```

## Cloud Deployment

### AWS Deployment

#### Using AWS App Runner (Recommended)

1. **Prepare the application**:
   ```bash
   # Create apprunner.yaml
   version: 1.0
   runtime: python3
   build:
     commands:
       build:
         - echo "Installing dependencies"
         - pip install -r requirements.txt
   run:
     runtime-version: 3.9
     command: uvicorn backend.main:app --host 0.0.0.0 --port 8000
     network:
       port: 8000
       env: PORT
   ```

2. **Deploy via AWS Console**:
   - Go to AWS App Runner
   - Create service from source code
   - Connect to your repository
   - Configure environment variables

## 🔧 Environment Configuration

### Required Environment Variables

**Backend** (stored in Azure Key Vault):
- `PINECONE_API_KEY`: Vector database access key
- `GOOGLE_API_KEY`: Google Gemini AI API key  
- `PINECONE_INDEX_NAME`: multilingual-e5-large-index
- `PINECONE_NAMESPACE`: gov-terms

**Frontend** (`.env` file):
```bash
REACT_APP_API_BASE_URL=https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io
```

### Azure Configuration Files

The project includes several Azure configuration files:

- `azure.yaml`: Main Azure Developer CLI configuration
- `infra/main.bicep`: Infrastructure as Code (Bicep templates)
- `infra/main.parameters.json`: Bicep parameters
- `.github/workflows/`: GitHub Actions for CI/CD

## 📋 Prerequisites for Deployment

1. **Azure CLI** installed and configured
2. **Azure Developer CLI** installed
3. **Docker** (for local testing)
4. **Node.js 16+** and **npm**
5. **Python 3.8+** and **pip**

### API Keys Setup

1. **Pinecone API Key**:
   - Sign up at [pinecone.io](https://pinecone.io)
   - Create a new project
   - Generate API key
   - Create index named `multilingual-e5-large-index`

2. **Google Gemini API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com)
   - Create new API key
   - Enable Gemini API access

## 🔒 Security & Configuration

### CORS Configuration

The backend is configured to allow requests from:
- `https://wonderful-water-00378c20f.2.azurestaticapps.net`
- `http://localhost:3000` (development)
- `https://*.azurestaticapps.net` (wildcard)

## 📊 Monitoring & Maintenance

### Health Checks

**Backend Health**:
```bash
curl https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io/health
```

Response includes:
- Service status
- Pinecone connection status  
- Vector database count (7,630 terms)
- Timestamp and version

### Logs Access

**Azure CLI**:
```bash
# Container App logs
az containerapp logs show --name cabackend-32p4pozukxrfi --resource-group RAGdb

# Static Web App logs
az staticwebapp show --name stapp32p4pozukxrfi --resource-group RAGdb
```

### Performance Monitoring

- **Application Insights**: `appi32p4pozukxrfi`
- **Log Analytics**: `log32p4pozukxrfi`
- **Container App Metrics**: CPU, Memory, Request count, Response time

## 🔒 Security Considerations

### Secrets Management
- All API keys stored in Azure Key Vault
- Container Apps use managed identity for Key Vault access
- No secrets in code or configuration files

### Network Security
- HTTPS enforced on all endpoints
- CORS properly configured
- Container Apps in managed environment

### Access Control
- Azure RBAC for resource management
- Static Web Apps deployment tokens for CI/CD

## 🚨 Troubleshooting

### Common Issues

1. **Backend Health Check Fails**:
   - Check Container App status in Azure Portal
   - Verify Pinecone API key in Key Vault
   - Check application logs

2. **Frontend Not Loading**:
   - Verify Static Web App deployment status
   - Check browser console for CORS errors
   - Confirm API base URL in frontend config

3. **API Responses Slow**:
   - Check Pinecone service status
   - Verify Gemini API quota
   - Review Container App scaling settings

### Emergency Contacts

- Azure Support: Portal support request
- Pinecone Support: support@pinecone.io
- Google AI Support: AI Studio documentation

### Version History

- **v2.0.0**: Current production version
  - Ultra-simplified backend architecture
  - Fixed CORS and endpoint issues
  - Optimized for Azure deployment
