import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate
from transformers import pipeline
import tiktoken

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def truncate_context(context_text: str, max_tokens: int =1000) -> str:
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





def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB with more results for better context
    results = db.similarity_search_with_relevance_scores(query_text, k=6)
    if len(results) == 0 or results[0][1] < 0.2:
        print(f"I couldn't provide any relevant information. Please refer the FAQ's for more information.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    # Truncate context to avoid token length issues
    truncated_context = truncate_context(context_text, max_tokens=250)
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=truncated_context, question=query_text)
    
    print("="*60)
    print("QUERY:", query_text)
    print("="*60)
    print("\nRetrieved Context:")
    print("-" * 40)
    print(truncated_context)
    print("-" * 40)

    # Prepare the local HuggingFace LLM with better parameters for structured responses
    hf_pipeline = pipeline(
        "text2text-generation", 
        model="google/flan-t5-large",
        max_length=2048,  # Longer for comprehensive responses
        do_sample=True,
        temperature=0.3,  # Balanced for structured responses
        top_p=0.9,
        repetition_penalty=1.2,
        no_repeat_ngram_size=2,
        early_stopping=False  # Allow longer responses
    )
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    try:
        response_text = llm.invoke(prompt)
        
        # Format the response to be more structured
        # formatted_response = format_response(response_text, query_text)
        
        # print(f"\nAnswer:\n{formatted_response}")
        
        print(f"\nSources:")
        for i, (doc, score) in enumerate(results, 1):
            source = doc.metadata.get("source", "Unknown")
            print(f"  {i}. {source} (relevance: {score:.3f})")
            
    except Exception as e:
        print(f"Error generating response: {e}")
        print("This might be due to the model not being able to process the input.")

def get_rag_response(query_text: str):
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_relevance_scores(query_text, k=6)
    if len(results) == 0 or results[0][1] < 0.2:
        return "Unable to find matching results.", []
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    truncated_context = truncate_context(context_text)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=truncated_context, question=query_text)
    hf_pipeline = pipeline(
        "text2text-generation", 
        model="google/flan-t5-base",
        max_length=1024,
        do_sample=True,
        temperature=0.3,
        top_p=0.9,
        repetition_penalty=1.2,
        no_repeat_ngram_size=2,
        early_stopping=False
    )
    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    response_text = llm.invoke(prompt)
    # formatted_response = format_response(response_text, query_text)
    sources = [
        {"source": doc.metadata.get("source", "Unknown"), "relevance": score}
        for doc, score in results
    ]
    return response_text, sources

if __name__ == "__main__":
    main()
