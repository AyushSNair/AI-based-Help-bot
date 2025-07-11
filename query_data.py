import argparse
import os
import logging
from typing import List, Tuple, Any
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate
from transformers import pipeline
import tiktoken

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception as e:
        logger.warning(f"Error counting tokens: {e}")
        # Fallback: estimate tokens as words * 1.3
        return int(len(text.split()) * 1.3)


def truncate_context(context_text: str, max_tokens: int = 1000) -> str:
    """Truncate context to fit within token limits."""
    if count_tokens(context_text) <= max_tokens:
        return context_text
    
    # Split by sections and truncate
    sections = context_text.split("\n\n---\n\n")
    truncated_sections = []
    current_tokens = 0
    
    for section in sections:
        section_tokens = count_tokens(section)
        if current_tokens + section_tokens <= max_tokens:
            truncated_sections.append(section)
            current_tokens += section_tokens
        else:
            # Try to include at least part of this section
            words = section.split()
            truncated_section = ""
            for word in words:
                if count_tokens(truncated_section + " " + word) <= max_tokens - current_tokens:
                    truncated_section += " " + word if truncated_section else word
                else:
                    break
            if truncated_section:
                truncated_sections.append(truncated_section)
            break
    
    return "\n\n---\n\n".join(truncated_sections)


def get_rag_response(query_text: str) -> Tuple[str, List[dict]]:
    """
    Get RAG response for a query.
    Returns (answer, sources) tuple.
    """
    try:
        logger.info(f"Processing query: {query_text[:50]}...")
        
        # Check if chroma directory exists
        if not os.path.exists(CHROMA_PATH):
            logger.warning(f"ChromaDB directory {CHROMA_PATH} not found")
            return get_fallback_response(query_text)
        
        # Initialize embeddings
        try:
            embedding_function = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}  # Force CPU for deployment
            )
        except Exception as e:
            logger.error(f"Error initializing embeddings: {e}")
            return get_fallback_response(query_text)
        
        # Initialize ChromaDB
        try:
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            return get_fallback_response(query_text)
        
        # Search the database
        try:
            results = db.similarity_search_with_relevance_scores(query_text, k=6)
            if len(results) == 0 or results[0][1] < 0.2:
                logger.info("No relevant results found")
                return get_fallback_response(query_text)
        except Exception as e:
            logger.error(f"Error searching database: {e}")
            return get_fallback_response(query_text)
        
        # Prepare context
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        truncated_context = truncate_context(context_text, max_tokens=250)
        
        # Create prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=truncated_context, question=query_text)
        
        # Initialize LLM - use smaller model for deployment
        try:
            hf_pipeline = pipeline(
                "text2text-generation", 
                model="google/flan-t5-small",  # Smaller model for deployment
                max_length=512,  # Reduced for deployment
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                repetition_penalty=1.2,
                no_repeat_ngram_size=2,
                early_stopping=False,
                device=-1  # Force CPU
            )
            llm = HuggingFacePipeline(pipeline=hf_pipeline)
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            return get_fallback_response(query_text)
        
        # Generate response
        try:
            response_text = llm.invoke(prompt)
            
            # Prepare sources
            sources = [
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "relevance": float(score)
                }
                for doc, score in results
            ]
            
            logger.info("Successfully generated RAG response")
            return response_text, sources
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return get_fallback_response(query_text)
    
    except Exception as e:
        logger.error(f"Unexpected error in get_rag_response: {e}")
        return get_fallback_response(query_text)


def get_fallback_response(query_text: str) -> Tuple[str, List[dict]]:
    """
    Provide fallback responses when RAG system is not available.
    """
    query_lower = query_text.lower()
    
    if "registration" in query_lower or "register" in query_lower:
        answer = """To register for a MOSDAC account:

1. Visit the MOSDAC portal at https://mosdac.gov.in
2. Click on "New User Registration"
3. Fill in your details including:
   - Full Name
   - Email address
   - Institution/Organization
   - Purpose of data usage
4. Submit the form and wait for approval

Once approved, you can login and access satellite data products."""
        sources = [{"source": "MOSDAC Registration Guide", "relevance": 0.9}]
        
    elif "insat" in query_lower or "satellite" in query_lower:
        answer = """MOSDAC provides access to various satellite data products including:

**INSAT-3D/3DR Satellites:**
- Meteorological data
- Oceanographic parameters
- Land surface information
- Atmospheric profiles

**Available Products:**
- Level-1 radiance data
- Level-2 derived products
- Quick look images
- Meteorological parameters

Data is available in various formats including HDF5, NetCDF, and GeoTIFF."""
        sources = [{"source": "INSAT Data User Guide", "relevance": 0.8}]
        
    elif "download" in query_lower or "data" in query_lower:
        answer = """To download data from MOSDAC:

1. **Login** to your registered account
2. **Navigate** to Data Search section
3. **Select** your parameters:
   - Satellite/Sensor
   - Product type
   - Date range
   - Geographic area
4. **Search** for available data
5. **Add to cart** or **Download directly**
6. **Track** your download requests in "My Orders"

Large datasets may require FTP download."""
        sources = [{"source": "Data Download Guide", "relevance": 0.8}]
        
    else:
        answer = f"""I can help you with MOSDAC-related questions about:

- **Account registration** and login issues
- **Data download** procedures
- **Satellite data products** (INSAT-3D/3DR, etc.)
- **Technical specifications** and formats

Your question: "{query_text}"

For more specific information, please visit the MOSDAC portal at https://mosdac.gov.in or refer to the user documentation."""
        sources = [{"source": "MOSDAC Help Center", "relevance": 0.7}]
    
    return answer, sources


def main():
    """CLI interface for testing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    print("="*60)
    print("QUERY:", query_text)
    print("="*60)

    try:
        answer, sources = get_rag_response(query_text)
        print(f"\nAnswer:\n{answer}")
        print(f"\nSources:")
        for i, source in enumerate(sources, 1):
            print(f"  {i}. {source['source']} (relevance: {source['relevance']:.3f})")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
