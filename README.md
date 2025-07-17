# Gov Terms AI 🏛️

**Gov Terms AI** is a comprehensive Retrieval-Augmented Generation (RAG) system designed to help users understand Australian government terminology, abbreviations, and acronyms. The system combines semantic search with AI-powered responses to provide accurate, contextual explanations of government terms.

## 🌟 Features

- 🔍 **Semantic Search**: Find relevant government terms using advanced vector similarity search
- 🤖 **AI-Enhanced Responses**: Get conversational explanations powered by Google's Gemini 2.0 Flash
- 🎯 **Intelligent Source Tracking**: AI automatically selects and displays the most relevant source for each response
- 📊 **Rich Knowledge Base**: 7,630+ government terms from Australian agencies
- 💬 **Chat Interface**: Intuitive chat-based user interface
- 🔧 **Modular Architecture**: Clean separation between frontend and backend
- 🚀 **Production Ready**: Deployed on Azure with Static Web Apps and Container Apps
- 🛡️ **Security Focused**: Comprehensive security audit and deployment best practices

## 🌐 Live Application

**Frontend**: https://wonderful-water-00378c20f.2.azurestaticapps.net  
**Backend**: https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io  

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Azure Static    │    │ Azure Container │    │  Pinecone Vector │
│   Web Apps      │◄──►│     Apps        │◄──►│    Database     │
│ React Frontend  │    │ FastAPI Backend │    │  7,630+ Terms   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                ▲
                                │
                       ┌─────────────────┐
                       │   Gemini 2.0    │
                       │     Flash       │
                       │  AI Responses   │
                       └─────────────────┘
```

### 🎯 Intelligent Source Selection Flow

1. **Query Processing**: User submits a question about government terminology
2. **Vector Search**: Pinecone returns top 3 most relevant sources with similarity scores
3. **AI Analysis**: Gemini 2.0 Flash analyzes all 3 sources and selects the most appropriate one
4. **Smart Response**: System returns structured response with selected source highlighted
5. **Frontend Display**: UI shows only the source that was actually used by the AI

## 📁 Project Structure

```
Gov-Terms-AI/
├── frontend/                    # React application (Azure Static Web Apps)
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── utils/api.js        # API service layer
│   │   └── components/         # React components
│   ├── package.json            # Frontend dependencies
│   └── public/                 # Static assets
├── backend/                     # FastAPI server (Azure Container Apps)
│   ├── app.py                  # Ultra-simplified FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Container configuration
├── infra/                      # Azure infrastructure (Bicep)
│   ├── main.bicep              # Main infrastructure template
│   └── main.parameters.json    # Infrastructure parameters
├── data/                       # Core data files
│   ├── glossary_data_combine.json  # Main government terms dataset
│   └── README.md               # Data documentation
├── scripts/                    # Deployment and utility scripts
│   ├── deploy-azure.ps1        # Azure deployment script
│   ├── update-backend-only.ps1 # Backend-only updates
│   ├── dev.py                  # Development server launcher
│   └── data_utils.py           # Data processing utilities
├── docs/                       # Documentation
│   ├── API.md                  # API documentation
│   ├── DEPLOYMENT.md           # Deployment guide
│   └── DEVELOPMENT.md          # Development guide
├── azure.yaml                 # Azure Developer CLI configuration
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **API Keys**: Pinecone, Google Gemini AI

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Gov-Terms-AI

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# PINECONE_API_KEY=your_pinecone_key
# GEMINI_API_KEY=your_gemini_key
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
cd backend
python main.py

# Server runs on http://localhost:8000
```

### 3. Frontend Setup

```bash
# Install Node.js dependencies
cd frontend
npm install

# Start React development server
npm start

# Frontend runs on http://localhost:3000
```

### 4. Access the Application

Open your browser to `http://localhost:3000` and start chatting with Gov Terms AI!

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required API Keys
PINECONE_API_KEY=your_pinecone_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configuration
PINECONE_INDEX_NAME=terms-e5-small-v2
PINECONE_NAMESPACE=__default__
BACKEND_HOST=localhost
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

### API Keys Setup

1. **Pinecone API Key**:
   - Sign up at [pinecone.io](https://www.pinecone.io/)
   - Create a new project
   - Get your API key from the dashboard

2. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Copy the key to your `.env` file

## 📊 Data Pipeline

### Setting Up the Knowledge Base

If you want to create your own embeddings from government glossary data:

```bash
# 1. Generate embeddings from glossary data
cd ml-pipeline
python generate_embeddings.py

# 2. Upload embeddings to Pinecone
python upload_to_pinecone.py

# 3. Test the upload
python upload_to_pinecone.py --test-only
```

### Using Existing Data

The system is designed to work with the existing Pinecone index containing 8000+ government terms. Simply provide your Pinecone API key and index name in the `.env` file.

## 🛠️ Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# View API documentation
# http://localhost:8000/docs
```

### Frontend Development

```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build
```

### Adding New Features

1. **Backend**: Add new endpoints in `backend/main.py` and business logic in `backend/services/`
2. **Frontend**: Add new components in `frontend/src/components/`
3. **Data**: Process new government terms using `ml-pipeline/` scripts

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Test API health
curl http://localhost:8000/health

# Test query endpoint with intelligent source selection
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What does NDIA stand for?"}'
```

### API Response Format

The `/api/query` endpoint now returns enhanced responses with intelligent source tracking:

```json
{
  "ai_response": "{\"definition\": \"NDIA: National Disability Insurance Agency\", \"elaboration\": \"The NDIA is responsible for implementing the National Disability Insurance Scheme (NDIS) in Australia.\", \"source_entity\": \"Department of Social Services\"}",
  "sources": [
    {
      "score": 0.987,
      "text": "NDIA",
      "entity": "Department of Social Services",
      "body_type": "Non-corporate Commonwealth entity",
      "portfolio": "Social Services",
      "url": "https://www.ndis.gov.au"
    },
    // ... 2 more sources for debugging
  ],
  "selected_source": {
    "score": 0.987,
    "text": "NDIA", 
    "entity": "Department of Social Services",
    "body_type": "Non-corporate Commonwealth entity",
    "portfolio": "Social Services",
    "url": "https://www.ndis.gov.au"
  }
}
```

**Key Features:**
- `ai_response`: JSON string containing definition, elaboration, and source_entity
- `sources`: All 3 retrieved sources (for debugging and transparency)  
- `selected_source`: The specific source that Gemini chose to base its response on

### Frontend Testing

```bash
cd frontend

# Run React tests
npm test

# Run build test
npm run build
```

## 🚀 Deployment

### Current Production Deployment

The application is currently deployed on **Microsoft Azure**:

**Frontend (Azure Static Web Apps)**:  
- URL: https://wonderful-water-00378c20f.2.azurestaticapps.net
- Technology: React.js built and deployed using SWA CLI
- Resource Group: RAGdb (East US 2)

**Backend (Azure Container Apps)**:  
- URL: https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io
- Technology: FastAPI in Docker container (v2.0.0)
- Resource Group: RAGdb (East US 2)
- Auto-scaling enabled

**Database**:  
- Pinecone Vector Database (7,630 government terms)
- Model: multilingual-e5-large-index
- Namespace: gov-terms

### Quick Deployment Commands

```bash
# Frontend deployment
cd frontend
npm run build
swa deploy build --deployment-token "YOUR_TOKEN" --env production

# Backend deployment (Docker)
docker build -t govterms-backend:latest -f backend/Dockerfile .
docker tag govterms-backend:latest cr32p4pozukxrfi.azurecr.io/govterms-backend:v2.0.0
docker push cr32p4pozukxrfi.azurecr.io/govterms-backend:v2.0.0

# Update Container App
az containerapp update --name cabackend-32p4pozukxrfi --resource-group RAGdb --image cr32p4pozukxrfi.azurecr.io/govterms-backend:v2.0.0
```

### Environment Configuration

**Frontend (.env)**:
```bash
REACT_APP_API_BASE_URL=https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io
```

**Backend (Azure Key Vault)**:
```bash
PINECONE_API_KEY=stored_in_azure_key_vault
GOOGLE_API_KEY=stored_in_azure_key_vault
PINECONE_INDEX_NAME=multilingual-e5-large-index
PINECONE_NAMESPACE=gov-terms
```

## 📖 API Documentation

### Main Endpoints

- **POST `/api/query`**: Main RAG endpoint for government term queries
- **GET `/health`**: System health check with Pinecone status
- **GET `/`**: Root endpoint with service info

### Example API Usage

```javascript
// Query government terms with RAG
const response = await fetch('/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "What does NDIA stand for?"
  })
});

const data = await response.json();
// Returns: { query, response, sources, timestamp }
// Sources include: term, definition, agency, score
```

### Health Check

```bash
curl https://cabackend-32p4pozukxrfi.redmushroom-cb7b0f31.eastus2.azurecontainerapps.io/health
# Returns: { status, timestamp, service, version, pinecone_status, vector_count }
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow Python PEP 8 style guide
- Use React functional components with hooks
- Add docstrings to Python functions
- Include error handling and logging
- Update tests for new features

## 🔍 Data Sources

The knowledge base contains government terms extracted from:

- **186+ Australian Government Agency Annual Reports**
- **Official government glossaries and websites**
- **Department-specific terminology databases**
- **Prime Minister & Cabinet abbreviations**

Source: [transparency.gov.au](https://www.transparency.gov.au/)

## 🛡️ Security

### Security Status & Audit

The project has undergone a comprehensive security audit. **See [SECURITY_AUDIT_SUMMARY.md](SECURITY_AUDIT_SUMMARY.md) for full details.**

**Key Security Features:**
- ✅ All secrets stored in Azure Key Vault or environment variables
- ✅ HTTPS enforcement via Azure Static Web Apps
- ✅ Docker multi-stage builds for minimal attack surface
- ✅ Input validation using Pydantic models
- ✅ Proper CORS configuration
- ✅ Robust deployment workflows with anti-caching measures

**NPM Audit Status:**
- 9 vulnerabilities detected (3 moderate, 6 high)
- **Assessment**: Development-only vulnerabilities, no production risk
- **Action**: No immediate fixes required (see audit summary)
- **Reason**: All vulnerabilities affect build tools, not runtime

**Security Best Practices:**
```bash
# Never commit secrets
echo "*.env*" >> .gitignore

# Use environment variables
export PINECONE_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"

# Regular security checks
npm audit
docker scan govterms-backend:latest
```

**Future Security Enhancements:**
- [ ] API rate limiting implementation
- [ ] User authentication system
- [ ] Enhanced input sanitization
- [ ] Security monitoring and logging
- [ ] Regular penetration testing

## 🆘 Troubleshooting

### Common Issues

1. **Backend won't start**:
   - Check if all required environment variables are set
   - Verify Python dependencies are installed
   - Check if port 8000 is available

2. **Frontend can't connect to backend**:
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Verify API base URL in frontend

3. **No search results**:
   - Check Pinecone API key and index name
   - Verify embeddings are uploaded to Pinecone
   - Check vector database connection

4. **Gemini API errors**:
   - Verify Gemini API key is valid
   - Check API quota and usage limits
   - Ensure proper error handling

### Debug Mode

```bash
# Backend debug mode
LOG_LEVEL=DEBUG python backend/main.py

# Frontend debug mode
REACT_APP_DEBUG=true npm start
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Hiren Bhavsar** - Policy Officer, Department of Social Services
- GitHub: [your-github-profile](https://github.com/your-username)
- Email: your.email@dss.gov.au

## 🙏 Acknowledgments

- **Australian Government** for providing open access to annual reports
- **Transparency.gov.au** for government data availability
- **Pinecone** for vector database services
- **Google** for Gemini AI API
- **Hugging Face** for transformer models (e5-small-V2)

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Gemini AI Documentation](https://ai.google.dev/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)

---

**Built with ❤️ for the Australian Government Community**
