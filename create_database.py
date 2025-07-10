from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import shutil
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
CHROMA_PATH = "chroma"
DATA_PATH = "data/books"  # Using forward slashes for cross-platform compatibility

# Optimized parameters for knowledge base content
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 1500
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def main():
    """Main function to orchestrate the RAG pipeline."""
    try:
        logger.info("Starting RAG pipeline for MOSDAC knowledge base...")
        generate_data_store()
        logger.info("RAG pipeline completed successfully!")
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise


def generate_data_store():
    """Generate the complete vector store from documents."""
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents() -> List[Document]:
    """Load all markdown documents from the data directory."""
    try:
        loader = DirectoryLoader(DATA_PATH, glob="*.md")
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from {DATA_PATH}")
        
        # Log document details
        for i, doc in enumerate(documents):
            logger.info(f"Document {i}: {doc.metadata.get('source', 'Unknown')} "
                       f"({len(doc.page_content)} characters)")
        
        return documents
    except Exception as e:
        logger.error(f"Failed to load documents: {str(e)}")
        raise


def split_text(documents: List[Document]) -> List[Document]:
    """
    Split documents into optimized chunks for knowledge base retrieval.
    
    Args:
        documents: List of Document objects to split
        
    Returns:
        List of chunked Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
        separators=[
            "\n\n",      # Double newlines (sections)
            "\n",        # Single newlines
            "### ",      # Markdown headers
            "## ",
            "# ",
            ". ",        # Sentences
            " ",         # Words
            ""           # Characters
        ]
    )
    
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    
    # Analyze chunk quality
    analyze_chunks(chunks)
    
    # Preview sample chunk (if available)
    if len(chunks) > 7:
        preview_chunk(chunks[7], 7)
    
    return chunks


def analyze_chunks(chunks: List[Document]) -> Dict[str, Any]:
    """Analyze chunk distribution and quality."""
    chunk_sizes = [len(chunk.page_content) for chunk in chunks]
    
    stats = {
        'total_chunks': len(chunks),
        'avg_size': sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0,
        'min_size': min(chunk_sizes) if chunk_sizes else 0,
        'max_size': max(chunk_sizes) if chunk_sizes else 0,
    }
    
    # Size distribution
    size_ranges = {
        "< 400": len([s for s in chunk_sizes if s < 400]),
        "400-600": len([s for s in chunk_sizes if 400 <= s < 600]),
        "600-800": len([s for s in chunk_sizes if 600 <= s < 800]),
        "800+": len([s for s in chunk_sizes if s >= 800])
    }
    
    logger.info(f"Chunk Analysis:")
    logger.info(f"  Total chunks: {stats['total_chunks']}")
    logger.info(f"  Average size: {stats['avg_size']:.0f} characters")
    logger.info(f"  Size range: {stats['min_size']} - {stats['max_size']} characters")
    
    logger.info(f"  Size distribution:")
    for range_name, count in size_ranges.items():
        percentage = (count / len(chunks)) * 100 if chunks else 0
        logger.info(f"    {range_name}: {count} chunks ({percentage:.1f}%)")
    
    return stats


def preview_chunk(chunk: Document, chunk_index: int):
    """Preview a specific chunk for quality assessment."""
    logger.info(f"\nSample chunk #{chunk_index}:")
    logger.info(f"  Content length: {len(chunk.page_content)} characters")
    logger.info(f"  Content preview: {chunk.page_content[:200]}...")
    logger.info(f"  Metadata: {chunk.metadata}")


def save_to_chroma(chunks: List[Document]):
    """Save chunks to Chroma vector database."""
    try:
        # Clear out the existing database
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            logger.info(f"Cleared existing database at {CHROMA_PATH}")
        
        # Initialize embeddings
        logger.info(f"Initializing embeddings with model: {EMBEDDING_MODEL}")
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}  # Explicitly set to CPU for consistency
        )
        
        # Create new database from chunks
        logger.info("Creating vector database...")
        db = Chroma.from_documents(
            chunks, 
            embeddings, 
            persist_directory=CHROMA_PATH
        )
        
        # Persist the database
        db.persist()
        logger.info(f"Successfully saved {len(chunks)} chunks to {CHROMA_PATH}")
        
        # Verify database creation
        verify_database(db, chunks)
        
    except Exception as e:
        logger.error(f"Failed to save to Chroma: {str(e)}")
        raise


def verify_database(db: Chroma, original_chunks: List[Document]):
    """Verify that the database was created correctly."""
    try:
        # Test a simple similarity search
        if original_chunks:
            test_query = "MOSDAC portal registration"
            results = db.similarity_search(test_query, k=3)
            logger.info(f"Database verification: Found {len(results)} results for test query")
            
            # Log first result for verification
            if results:
                logger.info(f"First result preview: {results[0].page_content[:100]}...")
        
    except Exception as e:
        logger.warning(f"Database verification failed: {str(e)}")


def load_existing_database() -> Chroma:
    """Load an existing Chroma database."""
    try:
        if not os.path.exists(CHROMA_PATH):
            raise FileNotFoundError(f"No database found at {CHROMA_PATH}")
        
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        
        logger.info(f"Loaded existing database from {CHROMA_PATH}")
        return db
        
    except Exception as e:
        logger.error(f"Failed to load existing database: {str(e)}")
        raise


if __name__ == "__main__":
    main()