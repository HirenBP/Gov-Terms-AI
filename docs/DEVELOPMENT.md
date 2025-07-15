# Development Guide

## Getting Started

This guide will help you set up the Gov Terms AI project for development.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Git

## Initial Setup

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd "Gov Terms AI"
   ```

2. **Run the setup script**:
   ```bash
   python scripts/setup.py
   ```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your API keys and configuration

## Environment Variables

Create a `.env` file with the following variables:

```bash
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=gov-terms

# Google Gemini Configuration
GOOGLE_API_KEY=your_google_api_key

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Logging
LOG_LEVEL=INFO
```

## Development Workflow

### Backend Development

1. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the backend**:
   ```bash
   python backend/main.py
   # or
   uvicorn backend.main:app --reload
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Frontend Development

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000

### Full Stack Development

Use the development script to run both servers:

```bash
python scripts/dev.py both
```

This will start both backend and frontend servers concurrently.

## Project Structure

```
Gov Terms AI/
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   └── utils/           # Utilities and configuration
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── utils/       # Frontend utilities
│   │   └── App.js       # Main application component
│   ├── public/          # Static assets
│   └── package.json     # Dependencies and scripts
├── ml-pipeline/         # Machine learning tools
├── scraping-tools/      # Web scraping utilities
├── data/               # Data files and samples
├── scripts/            # Development and utility scripts
├── docs/               # Documentation
└── requirements.txt    # Python dependencies
```

## Key Components

### Backend Components

- **main.py**: FastAPI application with route definitions
- **models/chat_models.py**: Pydantic models for API requests/responses
- **services/rag_service.py**: RAG (Retrieval-Augmented Generation) logic
- **utils/config.py**: Configuration management

### Frontend Components

- **App.js**: Main React application component
- **utils/api.js**: API service for backend communication

### ML Pipeline

- **generate_embeddings.py**: Generate vector embeddings for terms
- **upload_to_pinecone.py**: Upload embeddings to Pinecone database

## Development Tasks

### Adding New Features

1. **Backend**: Add new routes in `main.py`, create models in `models/`, implement logic in `services/`
2. **Frontend**: Create components in `components/`, update `App.js` for routing
3. **Data**: Add new data processing in `scripts/data_utils.py`

### Testing

#### Backend Testing
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

#### Frontend Testing
```bash
cd frontend
npm test
```

### Data Processing

#### Process New Data
```bash
python scripts/data_utils.py clean -i data/raw/new_data.json -o data/processed/new_data.json
```

#### Generate Embeddings
```bash
python ml-pipeline/generate_embeddings.py --input data/processed/terms.json --output data/embeddings/
```

#### Upload to Pinecone
```bash
python ml-pipeline/upload_to_pinecone.py --input data/processed/terms.json
```

### Web Scraping

```bash
python scraping-tools/scraper.py
```

## Debugging

### Backend Debugging

1. **Enable debug logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check API health**:
   ```bash
   curl http://localhost:8000/health
   ```

3. **Validate environment variables**:
   ```bash
   python -c "from backend.utils.config import settings; print(settings)"
   ```

### Frontend Debugging

1. **Check browser console** for JavaScript errors
2. **Verify API connection** in browser Network tab
3. **Use React Developer Tools** browser extension

### Common Issues

1. **Import errors**: Check virtual environment activation
2. **API connection issues**: Verify backend is running on correct port
3. **Empty search results**: Check Pinecone index has data
4. **Slow responses**: Check API key limits and network connectivity

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Use meaningful variable names

### JavaScript
- Use ES6+ features
- Follow React best practices
- Use async/await for API calls
- Handle errors gracefully

### General
- Write self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Use consistent naming conventions

## Git Workflow

1. **Create feature branch**:
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "Add new feature description"
   ```

3. **Push and create pull request**:
   ```bash
   git push origin feature/new-feature
   ```

## Performance Optimization

### Backend
- Use async/await for I/O operations
- Implement caching for frequent requests
- Optimize database queries
- Monitor response times

### Frontend
- Use React.memo for component optimization
- Implement lazy loading
- Optimize bundle size
- Cache API responses

## Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement input validation
- Sanitize user inputs
- Use HTTPS in production

## Deployment

See `DEPLOYMENT.md` for production deployment instructions.

## Contributing

1. Follow the code style guidelines
2. Add tests for new features
3. Update documentation
4. Create descriptive commit messages
5. Submit pull requests for review
