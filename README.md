# Langchain RAG Tutorial

A Retrieval-Augmented Generation (RAG) system using LangChain, ChromaDB, and HuggingFace models to create a question-answering system from your documents.

## Features

- **Document Processing**: Load and chunk markdown documents
- **Vector Storage**: Use ChromaDB for efficient similarity search
- **Local LLM**: Use HuggingFace models for text generation (no API keys required)
- **Smart Context Truncation**: Automatically handle token limits
- **Improved Prompts**: Better structured responses

## Install dependencies

1. **For MacOS users**: Install `onnxruntime` dependency for `chromadb` using:
    ```bash
    conda install onnxruntime -c conda-forge
    ```
    See this [thread](https://github.com/microsoft/onnxruntime/issues/11037) for additional help if needed.

2. **For Windows users**: Follow the guide [here](https://github.com/bycloudai/InstallVSBuildToolsWindows?tab=readme-ov-file) to install the Microsoft C++ Build Tools. Be sure to follow through to the last step to set the environment variable path.

3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Install markdown dependencies:
    ```bash
    pip install "unstructured[md]"
    ```

## Setup

1. **Create the database**:
    ```bash
    python create_database.py
    ```

2. **Query the database**:
    ```bash
    # Use the improved version (recommended)
    python query_data_improved.py "Your question here"
    
    # Or use the original version
    python query_data.py "Your question here"
    ```

## Example Usage

```bash
# Ask about MOSDAC data download process
python query_data_improved.py "Steps to download the INSAT-3DR dataset"

# Ask about registration process
python query_data_improved.py "How to register for MOSDAC account"

# Ask about technical specifications
python query_data_improved.py "What are the INSAT-3DR technical specifications"
```

## Project Structure

```
langchain-rag-tutorial/
├── data/
│   └── books/
│       └── mosdac.md          # Sample document about MOSDAC
├── chroma/                    # Vector database (created after running create_database.py)
├── create_database.py         # Script to create the vector database
├── query_data.py              # Original query script
├── query_data_improved.py     # Improved query script with better error handling
├── compare_embeddings.py      # Script to compare embeddings
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Improvements Made

1. **Fixed Deprecation Warnings**: Updated imports to use the latest LangChain packages
2. **Token Length Management**: Added automatic context truncation to prevent token overflow
3. **Better Error Handling**: Improved error messages and fallback behavior
4. **Enhanced Prompts**: More structured prompts for better responses
5. **Improved Model Parameters**: Better generation parameters to reduce repetition

## Troubleshooting

### Common Issues

1. **Token Length Errors**: The improved version automatically handles this by truncating context
2. **Model Loading Issues**: Make sure you have enough RAM (at least 4GB recommended)
3. **ChromaDB Issues**: Delete the `chroma/` folder and recreate the database if needed

### Performance Tips

- Use `query_data_improved.py` for better results
- The system works best with specific questions rather than very broad ones
- For large documents, consider adjusting the chunk size in `create_database.py`

## Tutorial Video

Here is a step-by-step tutorial video: [RAG+Langchain Python Project: Easy AI/Chat For Your Docs](https://www.youtube.com/watch?v=tcqEUSNCn8I&ab_channel=pixegami).

## Adding Your Own Documents

1. Place your markdown files in the `data/books/` directory
2. Run `python create_database.py` to rebuild the vector database
3. Start querying with your questions!

## License

This project is for educational purposes. Feel free to modify and use for your own projects.
