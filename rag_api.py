from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your RAG logic here
from query_data import get_rag_response  # You'd need to refactor your logic into a function

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-based-help-bot-full.onrender.com"],  # Only allow your deployed frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_endpoint(request: QueryRequest):
    return get_rag_response(request.query)
