# DocuMind

**AI-powered document intelligence using Retrieval-Augmented Generation (RAG).**

DocuMind is an AI-powered document intelligence platform that allows users to upload PDF documents and ask questions in natural language. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-aware answers using Large Language Models (LLMs).

Instead of relying entirely on an LLM's pre-trained knowledge, DocuMind grounds its responses in the content of the uploaded documents.

## Features

- **PDF Upload:** Upload and process PDF documents.
- **Text Extraction:** Extract text from PDF files.
- **Document Chunking:** Split extracted content into smaller, overlapping chunks for effective retrieval.
- **Semantic Embeddings:** Generate vector embeddings using Ollama's embedding models.
- **Vector Storage:** Store document chunks and embeddings in PostgreSQL using pgvector.
- **Semantic Search:** Retrieve relevant document chunks based on the user's question.
- **AI-Powered Answers:** Generate context-aware responses using an LLM.
- **Document Deduplication:** Use SHA-256 content hashing to identify duplicate documents and detect modified versions.
- **Context-Aware Responses:** Ground generated answers in retrieved document content.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API development |
| SQLAlchemy ORM | Database models and data access |
| PostgreSQL | Relational data storage |
| pgvector | Vector storage and similarity search |
| Ollama | Local LLM and embedding model runtime |
| Qwen 3 | Language model for answer generation |
| nomic-embed-text | Text embedding generation |
| PyMuPDF | PDF text extraction |
| RAG | Retrieval-Augmented Generation |

## Architecture

DocuMind follows a Retrieval-Augmented Generation pipeline.

### Document Ingestion

1. User uploads a PDF document.
2. PyMuPDF extracts text from the document.
3. Extracted text is split into smaller chunks with overlapping content.
4. Ollama generates vector embeddings for each chunk.
5. Document metadata, chunks, and embeddings are stored in PostgreSQL with pgvector.
6. SHA-256 hashing helps identify duplicate or modified documents.

### Question Answering

1. User submits a natural-language question.
2. The question is converted into a vector embedding.
3. pgvector performs similarity search to retrieve relevant document chunks.
4. Retrieved content is passed to the LLM as context.
5. The LLM generates an answer grounded in the retrieved document content.

## RAG Workflow

```text
                 DOCUMENT INGESTION

       PDF Upload
            |
            v
      Text Extraction
            |
            v
      Text Chunking
            |
            v
    Generate Embeddings
            |
            v
   PostgreSQL + pgvector


                QUESTION ANSWERING

      User Question
            |
            v
    Generate Embedding
            |
            v
      Vector Search
            |
            v
   Retrieve Relevant Chunks
            |
            v
      LLM + Context
            |
            v
     Contextual Answer
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- pgvector extension
- Ollama

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/documind.git
cd documind
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Create a PostgreSQL database and enable the pgvector extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Configure your database connection using an environment variable.

### 5. Set up Ollama

Install Ollama and pull the required models:

```bash
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

Ensure Ollama is running locally.

### 6. Start the application

```bash
uvicorn main:app --reload
```

The API will be available at:

- API: http://localhost:8000
- Interactive API documentation: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/rag/documents/upload` | Upload and process a PDF |
| POST | `/rag/chat` | Ask questions about uploaded documents |

## Future Enhancements

- Source citations with document and page references.
- Improved chunking and retrieval strategies.
- Similarity thresholds and reranking.
- Hybrid search combining keyword and semantic retrieval.
- Conversation history and multi-turn interactions.
- Streaming LLM responses.
- User authentication and document-level access control.
- Production deployment and monitoring.

## License

This project is licensed under the MIT License.