# PDF Reader Application Documentation

## Overview

This Streamlit application creates a chat interface that allows users to ask questions about PDF documents and receive relevant responses. The application uses LlamaIndex for document indexing and retrieval, and OpenAI's API for generating conversational responses based on the PDF content.

## Features

- **PDF Processing**: Automatically reads and extracts text from all PDF files in the application directory
- **Vector Search**: Indexes document content for efficient semantic retrieval
- **Interactive Chat Interface**: Clean, user-friendly chat UI built with Streamlit
- **Streaming Responses**: Real-time streaming of AI-generated responses
- **Context-Aware Answers**: Retrieves and synthesizes information from multiple relevant document sections


## Prerequisites

**Required Libraries:**

- streamlit
- llama-index
- PyPDF2
- OpenAI API key (set as environment variable)

**Installation:**

```bash
pip install streamlit llama-index-core pypdf2 openai
```


## Environment Setup

You must set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```


## Code Structure

### Main Components

1. **PDF Text Extraction** (`read_pdf_files` function)
    - Scans directory for PDF files
    - Extracts text content from each PDF
    - Returns list of dictionaries with file names and extracted text
2. **Document Processing** (in `main` function)
    - Converts extracted text into Document objects
    - Creates vector embeddings for semantic search
    - Sets up retrieval system for finding relevant content
3. **Streamlit Interface** (in `main` function)
    - Configures page layout and title
    - Manages chat history in session state
    - Handles user input and displays responses
4. **Query Engine Configuration**
    - Uses tree summarization for synthesizing responses
    - Implements streaming for real-time response generation
    - Sets retrieval parameters (top 3 most relevant chunks)

## How It Works

1. When launched, the application scans for PDF files in the current directory
2. PDF content is extracted, processed, and indexed for semantic search
3. User inputs a question in the chat interface
4. The system retrieves the most relevant text chunks from the PDFs
5. A response is generated based on the retrieved content
6. The response is streamed back to the user in real-time

## Usage Instructions

1. Place PDF files in the same directory as the script
2. Run the application with: `streamlit run app.py` (replace with your script name)
3. Access the web interface at the provided local URL (typically http://localhost:8501)
4. Type questions about the PDF content in the chat input
5. Receive AI-generated responses based on the PDF information

## Customization Options

You can modify the following parameters to customize behavior:

- **PDF Directory**: Change `pdf_dir = "."` to specify a different directory path
- **Retrieval Settings**: Adjust `similarity_top_k=3` to control how many document chunks are retrieved
- **Response Mode**: Change `response_mode="tree_summarize"` to other modes like "refine" or "compact"


## Troubleshooting

- **Empty Responses**: Ensure PDFs contain extractable text (not just scanned images)
- **OpenAI API Errors**: Verify your API key is correctly set as an environment variable
- **PDF Reading Errors**: Check console output for specific error messages on problematic files


## Example Use Cases

- **Legal Document Analysis**: Query contracts or legal documents for specific clauses
- **Research Paper Review**: Extract and summarize information from academic PDFs
- **Technical Documentation**: Create a question-answering system for product manuals or guides


## Error Handling

The application includes error handling for:

- PDF reading issues (corrupted files, permissions problems)
- API response generation failures
- General exceptions during processing

