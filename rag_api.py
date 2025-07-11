from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
# Import your RAG logic here
from query_data import get_rag_response  # You'd need to refactor your logic into a function

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG API",
    description="A Retrieval-Augmented Generation API for document Q&A",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only; restrict in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.get("/")
def root():
    """Root endpoint to check if the API is running"""
    return {
        "message": "RAG API is running successfully!",
        "status": "healthy",
        "endpoints": {
            "query": "/query",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is operational"}

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    """Query endpoint for RAG responses"""
    try:
        logger.info(f"Received query: {request.query}")
        
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        answer, sources = get_rag_response(request.query)
        
        logger.info(f"Generated response for query: {request.query[:50]}...")
        
        return QueryResponse(answer=answer, sources=sources)
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/favicon.ico")
def favicon():
    """Handle favicon requests"""
    return {"message": "No favicon available"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
