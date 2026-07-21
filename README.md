# Gov Terms AI 🏛️

**Gov Terms AI** helps people understand Australian Government terminology, abbreviations and acronyms.

It combines semantic search with AI-generated explanations to provide clear, contextual answers based on a curated collection of Australian Government terms.

## Live application

Try Gov Terms AI here:

**https://hirenbp.github.io/Gov-Terms-AI/**

## Features

- 🔍 **Semantic search** — finds relevant government terms based on meaning, not only exact keywords
- 🤖 **AI-generated explanations** — uses Gemini 3.0 Flash to provide clear, conversational responses
- 🎯 **Source-aware answers** — identifies the source used to support each response
- 📚 **Government terminology database** — includes thousands of terms collected from Australian Government sources
- 💬 **Simple chat interface** — lets users ask questions in plain English
- 🌐 **Browser-based access** — available through GitHub Pages without installation

## How it works

1. A user asks a question about an Australian Government term, abbreviation or acronym.
2. The backend searches the Pinecone vector database for the most relevant entries.
3. Gemini 3.0 Flash uses the retrieved information to generate a clear explanation.
4. The application displays the answer together with the most relevant source.

## Technology

### Frontend

- React
- Vite
- GitHub Pages

### Backend

- Python
- FastAPI
- FastAPI Cloud

### AI and search

- Google Gemini 3.0 Flash
- Pinecone vector database
- Multilingual E5 embeddings

## Project structure

```text
Gov-Terms-AI/
├── frontend/                 # React and Vite frontend
│   ├── public/               # Static assets
│   ├── src/                  # Components and application logic
│   ├── package.json          # Frontend dependencies and scripts
│   └── vite.config.*         # Vite configuration
├── backend/                  # FastAPI backend
│   ├── main.py               # FastAPI application entry point
│   └── requirements.txt      # Python dependencies
├── data/                     # Government terminology data
├── scripts/                  # Data-processing and utility scripts
├── docs/                     # Supporting documentation
└── README.md                 # Project overview
```

The exact structure may vary as the project continues to develop.

## Run the project locally

### Prerequisites

You will need:

- Python 3.8 or later
- Node.js 16 or later
- A Pinecone API key
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/hirenbp/Gov-Terms-AI.git
cd Gov-Terms-AI
```

### 2. Set up the backend

Create a backend environment file and add the required API keys.

```env
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_api_key
PINECONE_INDEX_NAME=multilingual-e5-large-index
PINECONE_NAMESPACE=gov-terms
```

Install the Python dependencies and start the API:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will usually be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation will usually be available at:

```text
http://localhost:8000/docs
```

### 3. Set up the frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will display the local development URL in the terminal, commonly:

```text
http://localhost:5173
```

### 4. Configure the frontend API URL

Set the frontend environment variable used by the application to point to the local backend.

For example:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Check the frontend source code and existing environment files for the exact variable name used by the project.

## Available scripts

From the `frontend` directory:

```bash
npm run dev
```

Starts the Vite development server.

```bash
npm run build
```

Creates a production build.

```bash
npm run preview
```

Previews the production build locally.

```bash
npm run deploy
```

Deploys the frontend to GitHub Pages when the project is configured to use the `gh-pages` package.

Check `frontend/package.json` to confirm the deployment script and GitHub Pages configuration used by the repository.

## API overview

The backend provides endpoints for submitting terminology questions and checking service health.

Common endpoints include:

- `POST /api/query` — submits a user question to the RAG system
- `GET /health` — checks whether the backend and connected services are available
- `GET /docs` — opens FastAPI's interactive API documentation

Example request:

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What does NDIA stand for?"}'
```

## Data sources

The knowledge base is built from publicly available Australian Government material, including:

- agency annual reports
- official government glossaries
- departmental websites
- terminology and abbreviation lists
- material published through the Australian Government Transparency Portal

Source material remains the property of the relevant Australian Government bodies.

## Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your updates.
4. Commit your changes with a clear message.
5. Push the branch to your fork.
6. Open a pull request describing the change.

Please keep contributions focused, clearly documented and consistent with the existing project structure.

Useful contribution areas include:

- improving accessibility
- adding or validating government terminology
- improving search relevance
- refining source attribution
- improving error messages
- adding tests
- updating documentation

## Security

Do not commit API keys, credentials or local environment files to the repository.

Keep secrets in environment variables or in the secret-management system provided by the hosting platform.

Recommended checks include:

```bash
npm audit
```

and reviewing Python dependencies regularly for known vulnerabilities.

Potential future improvements include:

- API rate limiting
- stronger input validation
- improved monitoring and logging
- automated testing
- automated dependency checks

## Troubleshooting

### The frontend cannot connect to the backend

- Confirm the backend is running.
- Check the frontend API base URL.
- Confirm the production backend URL is allowed by the FastAPI CORS configuration.
- Check the browser console for network or CORS errors.

### The GitHub Pages site shows a blank page or returns missing-file errors

- Confirm the Vite `base` setting matches `/Gov-Terms-AI/`.
- Confirm the production build completed successfully.
- Confirm the correct build folder is being published.
- Check the browser console for incorrect asset paths.

### No search results are returned

- Confirm the Pinecone API key, index name and namespace.
- Check that the vector index contains the expected records.
- Review backend logs for embedding or query errors.

### Gemini requests fail

- Confirm the API key is valid.
- Check current usage limits and quotas.
- Review backend logs for the full error response.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Australian Government agencies for publishing accessible public information
- the Australian Government Transparency Portal
- Google for the Gemini API
- Pinecone for vector search infrastructure
- FastAPI and the open-source Python community
- React and Vite contributors

---

Built to make Australian Government language easier to understand.
