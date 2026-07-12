# GitHub Copilot Instructions for Gov Terms AI

This file provides context and guidelines for GitHub Copilot when working on the Gov Terms AI project.

## Project Overview

Gov Terms AI is a comprehensive system for understanding government terminology through AI-powered search and conversation. The project combines web scraping, machine learning, and conversational AI to help users understand complex government terms and concepts.

## Architecture

- **Backend**: FastAPI with RAG (Retrieval-Augmented Generation) using Pinecone and Google Gemini
- **Frontend**: React.js with modern UI components
- **ML Pipeline**: Embedding generation and vector database management
- **Database**: Pinecone vector database for term storage and retrieval

## Key Technologies

- **Python**: FastAPI, Pydantic, Pinecone, Google Generative AI
- **JavaScript**: React, Axios for API calls
- **ML**: Sentence transformers, vector embeddings


## Coding Guidelines

### Python Code
- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use Pydantic models for data validation
- Implement proper error handling with try-catch blocks
- Use environment variables for configuration
- Add comprehensive docstrings for modules and functions
- Use logging for debugging and monitoring

### React Code
- Use functional components with hooks
- Implement proper error boundaries
- Use async/await for API calls
- Maintain clean separation between UI and business logic
- Use proper state management
- Implement loading states and error handling

### General Principles
- Write self-documenting code with clear variable names
- Include error handling for all external dependencies
- Use configuration files for environment-specific settings
- Implement proper logging throughout the application
- Follow the DRY (Don't Repeat Yourself) principle
- Write modular, reusable code

## File Organization

```
Gov Terms AI/
├── backend/          # FastAPI application
│   ├── main.py      # FastAPI app and routes
│   ├── models/      # Pydantic models
│   ├── services/    # Business logic
│   └── utils/       # Utilities and configuration
├── frontend/        # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   └── utils/       # Frontend utilities
│   └── public/      # Static assets
├── ml-pipeline/     # ML and embedding tools
├── scraping-tools/  # Web scraping utilities
├── data/           # Datasets and sample data
└── scripts/        # Utility scripts
```

## API Design Patterns

### Request/Response Models
Always use Pydantic models for API endpoints:

```python
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[SourceDocument]
    conversation_id: str
```

### Error Handling
Implement consistent error responses:

```python
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )
```

## Environment Variables

Use descriptive environment variable names:
- `PINECONE_API_KEY`: Pinecone vector database API key
- `GOOGLE_API_KEY`: Google Gemini API key
- `PINECONE_INDEX_NAME`: Name of the Pinecone index
- `EMBEDDING_MODEL`: Model name for generating embeddings

## Testing Guidelines

### Backend Testing
- Test all API endpoints with various input scenarios
- Mock external dependencies (Pinecone, Gemini API)
- Test error handling and edge cases
- Validate Pydantic model serialization/deserialization

### Frontend Testing
- Test component rendering and user interactions
- Mock API calls for isolated testing
- Test error states and loading conditions
- Verify accessibility and responsive design

## Security Considerations

- Never commit API keys or sensitive data to version control
- Use environment variables for all secrets
- Implement input validation and sanitization
- Use HTTPS for all external API calls
- Implement proper CORS configuration

## Performance Guidelines

- Use async/await for I/O operations
- Implement caching where appropriate
- Optimize vector search queries
- Use lazy loading for large datasets
- Monitor API response times and set timeouts

## Documentation Standards

- Include README files in each major directory
- Document all API endpoints with examples
- Provide setup and deployment instructions
- Include troubleshooting guides
- Maintain up-to-date dependency lists

## Common Patterns

### FastAPI Route Pattern
```python
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Business logic here
        return ChatResponse(...)
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### React Component Pattern
```javascript
const Component = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    
    const handleAction = async () => {
        try {
            setLoading(true);
            setError(null);
            // API call here
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        // JSX here
    );
};
```

## Dependencies

Keep dependencies up to date and well-documented:
- Pin major versions to avoid breaking changes
- Regularly audit for security vulnerabilities
- Document the purpose of each dependency
- Use virtual environments for Python
- Use package-lock.json for Node.js

This project emphasizes clean, maintainable code with proper error handling, comprehensive documentation, and adherence to best practices for both backend and frontend development.
