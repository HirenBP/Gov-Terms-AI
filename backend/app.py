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
PINECONE_INDEX_NAME = "all-e5-large"
PINECONE_NAMESPACE = "gov-terms2"

# Validate configs
if not PINECONE_API_KEY or not GEMINI_API_KEY:
    raise ValueError("PINECONE_API_KEY and GEMINI_API_KEY are required")

# Initialize services
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX_NAME)
genai.configure(api_key=GEMINI_API_KEY) # type: ignore
gemini_model = genai.GenerativeModel('gemini-2.0-flash') # type: ignore

# FastAPI app
app = FastAPI(title="Gov Terms AI", version="2.1.0")
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
            "version": "2.1.0",
            "Deployment Date": "15 July 2025",
            "pinecone_status": "connected",
            "vector_count": index_stats.total_vector_count if hasattr(index_stats, 'total_vector_count') else "unknown"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Gov Terms AI Backend", "status": "running", "version": "2.1.0", "Deployment Date": "15 July 2025"}

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
            namespace="gov-terms2",
            query={
                "inputs": {"text": user_query},
                "top_k": 3
            } # type: ignore
        )
        hits = records.get('result', {}).get('hits', [])
        for hit in hits:
            score = hit.get('_score')
            fields = hit.get('fields', {})
            reference_text.append({
                "score": round(score, 3),
                "text": fields.get("text", ""),
                "entity": fields.get("Entity", ""),
                "body_type": fields.get("BodyType", ""),
                "portfolio": fields.get("Portfolio", ""),
                "url": fields.get("Url", "")
            })
         # Sort reference_text by score in descending order
        reference_text.sort(key=lambda x: x["score"], reverse=True)
        logger.info(f"✅ Found {len(reference_text)} relevant terms")
        logger.info(f"{reference_text}")
        return reference_text
    except Exception as e:
        logger.error(f"Database search failed: {e}")
        raise HTTPException(status_code=500, detail="Database search failed")

def send_gemini_prompt(user_query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Function 4: Send prompt to Gemini with search results as context."""
    try:
        # Build context from search results
        if search_results:
            context = "\n".join([
                f"{term['text']} Score: {term['score']} Entity: {term['entity']} BodyType:{term['body_type']} "
                for term in search_results
            ])
            
            prompt =f"""
            You are an expert AI assistant for defining Australian government terminology. Your mission is to provide a clear and concise definition for a given term, acting as a trusted resource for the public.

                Primary Goal:
                Your task is to define the term provided in the "User Query" using only the information available 
                in the "Reference Context".

                Critical Rules:

                Strict Sourcing: Use the "Reference Context" to identify and select the correct term definition. If the 
                term is not defined there, you must respond with the exact phrase: "I apologise, but the term 
                you're asking about is not defined in the knowledge I currently have."

                Elaboration Guidelines: For the elaboration field, you may use your general knowledge to provide 
                a helpful 1-2 sentence explanation of what the term is or what it does. The elaboration should be 
                informative and help the public understand the concept, even if the Reference Context doesn't 
                contain detailed explanatory information.

                Tone: Your tone must be helpful, professional, and easy for a member of the public to understand.

                Definition Selection Logic:
                Your first and most important step is to classify the User Query and then follow the appropriate
                  set of rules below.

                Step 1: Classify the User Query

                First, determine if the query is an 'ACRONYM' or a 'GENERAL TERM'.

                An 'ACRONYM' is a short-form abbreviation, usually in all-caps (e.g., 'IGA', 'PBS', 'ATO').

                A 'GENERAL TERM' is a standard word or phrase (e.g., 'tax', 'grant', 'commonwealth entity').

                Step 2: Apply Logic Based on Classification

                IF the query is an 'ACRONYM':
                Follow these rules in precise sequential order:

                Prioritise Generality: First, identify the definition with the shortest definition text.
                A shorter, more concise definition is considered more foundational.

                Break Ties with Score: If multiple definitions share the same shortest length, select 
                the one with the highest 'score' from that group.

                Conditionally Break Ties with Entity Type: If a tie still persists, check if all tied candidates
                  have a populated 'BodyType' field. If they do, choose the 'Non-corporate Commonwealth entity'.
                    Otherwise, skip this rule.

                Final Tie-Breaker: If the tie still cannot be resolved, select the definition from the more
                  central government body (e.g., 'Department of the Prime Minister and Cabinet').

                IF the query is a 'GENERAL TERM':
                Follow these rules in precise sequential order:

                Prioritise Highest Score: First, identify the definition with the highest 'score'.

                Break Ties with Entity Type: If multiple definitions share the exact same highest score, check 
                if all tied candidates have a populated 'BodyType' field. If they do, choose the 'Non-corporate
                  Commonwealth entity'. Otherwise, skip this rule.

                Final Tie-Breaker: If the tie still cannot be resolved, select the definition from the more
                  central government body (e.g., 'Department of the Prime Minister and Cabinet').

                **Response Format:**
                After choosing the correct source document using the logic above, you **must** structure your final output as a single JSON object. Do not include any text or formatting outside of this JSON object. The JSON must have the following structure:

                * A top-level key `"definition"` containing ONLY the term expansion or short definition (e.g., "NDIS: National Disability Insurance Scheme" or "Tax: A compulsory financial charge").
                * A top-level key `"elaboration"` containing 1-2 sentences that provide a general explanation of what the term is or what it does. Use your knowledge to make this explanation helpful and informative for the public, even if the Reference Context lacks detailed explanatory information.
                * A top-level key `"source_entity"` containing only the **string value** of the `entity` field from the source document you chose.

                **Example JSON Output Structure:**
                ```json
                {{
                "definition": "NDIS: National Disability Insurance Scheme",
                "elaboration": "This is a scheme that provides services and support for people with permanent and significant disability, their families and carers. It aims to help people with disability achieve their goals and participate more fully in the community.",
                "source_entity": "Department of Social Services"
                }}

                User Query: "{user_query}"

                Reference Context:
                {context}
                        """
        # Generate response
        response = gemini_model.generate_content(prompt) # type: ignore
        logger.info("✅ Gemini response generated")
        logger.info(f"The context was: {context}") # type: ignore
        
        # Parse JSON response from Gemini
        try:
            gemini_data = json.loads(response.text)
            selected_source_entity = gemini_data.get("source_entity")
            
            # Find which source was selected by matching entity
            selected_source = None
            if selected_source_entity:
                for source in search_results:
                    if source["entity"] == selected_source_entity:
                        selected_source = source
                        break
            
            return {
                "ai_response": response.text,
                "selected_source": selected_source
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw response without selected source
            return {
                "ai_response": response.text,
                "selected_source": None
            }
            
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
        gemini_result = send_gemini_prompt(user_query, search_results)
        
        # Log response received from Gemini 
        logger.info(f"Gemini Response is: {gemini_result['ai_response']}")
        logger.info(f"Selected source: {gemini_result['selected_source']}")
        
        # Structure and send response to frontend
        response_payload = {
            "ai_response": gemini_result["ai_response"], 
            "sources": search_results,  # All 3 sources for debugging
            "selected_source": gemini_result["selected_source"]  # The source Gemini actually used
        }
        logger.info(f"The sources are {response_payload['sources']} type of score is {response_payload['sources'][0]['score'] if response_payload['sources'] else 'N/A'}")
        return response_payload

    
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)