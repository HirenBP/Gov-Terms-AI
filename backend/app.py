#!/usr/bin/env python3
"""
Gov Terms AI - Ultra-Simplified Backend
Core RAG pipeline with 4 functions only.
"""

import os
import logging
from datetime import datetime
from typing import List, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pinecone import Pinecone
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_INDEX_NAME = "multilingual-e5-large-index"
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "gov-terms")

# Validate configs
if not PINECONE_API_KEY or not GEMINI_API_KEY:
    raise ValueError("PINECONE_API_KEY and GEMINI_API_KEY are required")

# Initialize services
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX_NAME)
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# FastAPI app
app = FastAPI(title="Gov Terms AI", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://wonderful-water-00378c20f.2.azurestaticapps.net",  # Main static web app
        "https://polite-tree-0976a390f.1.azurestaticapps.net",      # Secondary static web app
        "https://*.azurestaticapps.net"  # Wildcard for all Azure Static Web Apps
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancers."""
    try:
        # Basic health check - verify Pinecone connection
        index_stats = pinecone_index.describe_index_stats()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Gov Terms AI Backend",
            "version": "2.0.0",
            "pinecone_status": "connected",
            "vector_count": index_stats.total_vector_count if hasattr(index_stats, 'total_vector_count') else "unknown"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Gov Terms AI Backend", "status": "running", "version": "2.0.0"}

# ============================================================================
# Core 3 Functions
# ============================================================================

def get_user_query(request_body: dict) -> str:
    """Function 1: Get user query from frontend request."""
    try:
        query = request_body.get("query", "").strip()
        if not query:
            raise ValueError("Query is required")
        logger.info(f"Received query: {query[:50]}...")
        return query
    except Exception as e:
        logger.error(f"Error getting user query: {e}")
        raise HTTPException(status_code=400, detail="Invalid query")



def search_database(user_query) -> List[Dict[str, Any]]:
    """Function 3: Search Pinecone database."""
    try:
        reference_text = []
        records = pinecone_index.search_records(
            namespace="gov-terms",
            query={
                "inputs": {"text": user_query},
                "top_k": 3
            }
        )
        hits = records.get('result', {}).get('hits', [])
        for hit in hits:
            score = hit.get('_score')
            fields = hit.get('fields', {})
            reference_text.append({
                "score": round(score, 3),
                "id": fields.get("ID"),
                "text": fields.get("text"),
                "definition": fields.get("Definition"),
                "entity": fields.get("Entity"),
                "body_type": fields.get("BodyType"),
                "portfolio": fields.get("Portfolio"),
                "url": fields.get("Url")
            })

        logger.info(f"✅ Found {len(reference_text)} relevant terms")
        return reference_text
    except Exception as e:
        logger.error(f"Database search failed: {e}")
        raise HTTPException(status_code=500, detail="Database search failed")

def select_best_source(search_results: List[Dict[str, Any]], ai_response: str = None) -> dict:
    """Select the source used by Gemini (highest score, or match entity in Gemini response if tied)."""
    if not search_results:
        return None
    max_score = max(s['score'] for s in search_results)
    top_sources = [s for s in search_results if s['score'] == max_score]
    # If only one, return it
    if len(top_sources) == 1:
        return top_sources[0]
    # If tie, try to match entity in Gemini response
    if ai_response:
        for src in top_sources:
            entity = src.get('entity')
            if entity and entity in ai_response:
                return src
    # Fallback: return the first
    return top_sources[0]

def structure_response(user_query: str, ai_response: str, search_results: List[Dict[str, Any]]) -> dict:
    """Structure the API response to include only the used source."""
    not_defined_msg = "I apologize, but the term you're asking about is not defined in the knowledge I currently have."
    if ai_response and ai_response.strip() == not_defined_msg:
        source = None
    else:
        source = select_best_source(search_results, ai_response)
    return {
        "query": user_query,
        "response": ai_response,
        "sources": [source] if source else [],
        "timestamp": datetime.now().isoformat()
    }

def send_gemini_prompt(user_query: str, search_results: List[Dict[str, Any]]) -> str:
    """Function 4: Send prompt to Gemini with search results as context."""
    try:
        # Build context from search results
        if search_results:
            context = "\n".join([
                f"**{term['text']}** ({term['entity']}): {term['definition']} (Score: {term['score']:.3f})"
                for term in search_results
            ])
            
            prompt = f"""`
You are an AI assistant specializing in Australian government terminology. Your primary goal is to provide clear and concise definitions based *only* on the provided "Reference text."
Here are your guidelines:
1.  **Definition Retrieval:** Search the "Reference text" for a definition of the "User Question."
2.  **Definition Priority:** If multiple definitions for the same term exist within the "Reference text," identify the one with the highest 'score'. If multiple definitions share the exact same highest score, choose the Non-corporate commonwealth entity first.
3.  **No Definition Found:** If the term is not defined in the "Reference text," politely state, "I apologize, but the term you're asking about is not defined in the knowledge I currently have."
4.  **Response Structure and Formatting:**
    * Start by providing the precise definition. Such as ABN : Australian Business Number.
    * After the definition insert a new line.
    * On this new line, provide one or two additional sentences that offer further context or implications of the term within the Australian government (do not simply rephrase the definition).
5.  **Tone:** Maintain a helpful, polite, and conversational tone throughout your response, as if you are assisting a member of the public.
User Question: "{user_query}"
Reference text:
{context}
"""
        # Generate response
        response = gemini_model.generate_content(prompt)
        logger.info("✅ Gemini response generated")
        return response.text
    except Exception as e:
        logger.error(f"Gemini prompt failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

# ============================================================================
# API Endpoints
# ============================================================================

@app.post("/api/query")
async def query_endpoint(request: dict):
    """Main endpoint: RAG pipeline with 4 functions."""
    try:
        # Function 1: Get user query from frontend
        user_query = get_user_query(request)
        
        # Function 2: Search database
        search_results = search_database(user_query)
        
        # Function 3: Send Gemini prompt with context
        ai_response = send_gemini_prompt(user_query, search_results)
        
        # Log response received from Gemini 
        logger.info(f"Gemini Response is: {ai_response}")
        # Structure and send response to frontend
        response_payload = structure_response(user_query, ai_response, search_results)
        logger.info(f"The sources are {response_payload['sources']} type of score is {response_payload['sources'][0]['score'] if response_payload['sources'] else 'N/A'}")
        return response_payload

    
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)