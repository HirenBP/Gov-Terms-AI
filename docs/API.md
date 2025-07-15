# API Documentation

## Overview

The Gov Terms AI backend provides a REST API for retrieving government term definitions and engaging in conversational AI about government topics.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required for the API endpoints.

## Endpoints

### Health Check

Check if the API is running.

**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Root Endpoint

Basic API information.

**GET** `/`

**Response:**
```json
{
  "message": "Gov Terms AI API",
  "version": "1.0.0",
  "status": "running"
}
```

### Query Endpoint

Send a query and receive an AI-generated response with relevant sources.

**POST** `/api/query`

**Request Body:**
```json
{
  "query": "What is the Federal Register?"
}
```

**Response:**
```json
{
  "query": "What is the Federal Register?",
  "response": "The Federal Register is the daily journal of the United States government...",
  "sources": [
    {
      "term": "Federal Register",
      "definition": "The Federal Register is the daily journal...",
      "score": 0.95
    }
  ]
}
```

**Error Response:**
```json
{
  "error": "Invalid request",
  "detail": "Query cannot be empty"
}
```

## Error Codes

- `400 Bad Request`: Invalid request parameters
- `422 Unprocessable Entity`: Request validation failed
- `500 Internal Server Error`: Server error (API keys, database issues, etc.)

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## Data Models

### QueryRequest
```python
class QueryRequest(BaseModel):
    query: str  # User's query/question
```

### QueryResponse
```python
class QueryResponse(BaseModel):
    query: str  # Original user query
    response: str  # AI-generated response
    sources: List[SourceDocument]  # Relevant source documents
```

### SourceDocument
```python
class SourceDocument(BaseModel):
    term: str  # Government term
    definition: str  # Term definition
    score: Optional[float] = None  # Relevance score
```

## Usage Examples

### cURL Examples

**Health Check:**
```bash
curl -X GET http://localhost:8000/health
```

**Root Endpoint:**
```bash
curl -X GET http://localhost:8000/
```

**Query:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is an executive order?"}'
```

### JavaScript Examples

**Using Fetch:**
```javascript
// Query
const response = await fetch('/api/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'What is the Administrative Procedure Act?'
  })
});
const data = await response.json();

// Health check
const healthResponse = await fetch('/health');
const healthData = await healthResponse.json();
```

### Python Examples

**Using requests:**
```python
import requests

# Query
response = requests.post('http://localhost:8000/api/query', json={
    'query': 'Explain the notice and comment process'
})
data = response.json()

# Health check
health_response = requests.get('http://localhost:8000/health')
health_data = health_response.json()
```

## Configuration

The API uses the following environment variables:

- `PINECONE_API_KEY`: Required for vector database access
- `GOOGLE_API_KEY`: Required for Gemini AI responses
- `PINECONE_INDEX_NAME`: Name of the Pinecone index (default: "gov-terms")
- `EMBEDDING_MODEL`: Model for generating embeddings (default: "all-MiniLM-L6-v2")

## Development

To run the API in development mode:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Start the server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Deployment

For production deployment, consider:

- Using a production ASGI server (Gunicorn + Uvicorn)
- Implementing proper logging and monitoring
- Adding authentication and rate limiting
- Using environment-specific configuration
- Setting up health checks and monitoring

## Troubleshooting

### Common Issues

1. **500 Error on Chat**: Check that `PINECONE_API_KEY` and `GOOGLE_API_KEY` are set correctly
2. **Empty Search Results**: Ensure the Pinecone index contains data
3. **Slow Responses**: Check Pinecone and Gemini API response times

### Debugging

Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
