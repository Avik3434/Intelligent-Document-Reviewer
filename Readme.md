# Intelligent Document Reviewer

An end-to-end **Retrieval-Augmented Generation (RAG)** application that enables users to ask questions about PDF and text documents using semantic search and Large Language Models (LLMs).

The application extracts text from documents, performs OCR on scanned PDFs when necessary, splits the content into token-aware chunks, generates dense vector embeddings, stores them in a ChromaDB vector database, retrieves the most relevant information using semantic similarity search, reranks the retrieved results with a Cross-Encoder, and finally generates grounded answers using a Large Language Model.

This project was built to gain a deep understanding of the complete RAG pipeline by implementing each component from scratch rather than relying heavily on high-level frameworks.

---

# Features

- 📄 PDF document support
- 📝 TXT document support
- 🔍 OCR fallback for scanned PDFs
- ✂️ Token-aware chunking with overlap
- 🧠 Dense embeddings using **BAAI/bge-m3**
- 🗂 Persistent vector storage with **ChromaDB**
- 🚫 Duplicate document detection
- 🔎 Semantic similarity search
- 🎯 Cross-Encoder reranking using **BAAI/bge-reranker-base**
- 🤖 Context-aware answer generation using **Groq LLM**
- 📑 Metadata-rich document indexing
- 🏗 Clean and modular project architecture

---

# Architecture

```text
             PDF / TXT
                 │
                 ▼
       Document Extraction
                 │
                 ▼
      OCR (if document is scanned)
                 │
                 ▼
      Token-aware Chunking
                 │
                 ▼
        BGE-M3 Embeddings
                 │
                 ▼
     ChromaDB Vector Store
                 │
                 ▼
      Semantic Retrieval
          (Top K Chunks)
                 │
                 ▼
   Cross-Encoder Reranking
                 │
                 ▼
      Context Construction
                 │
                 ▼
          Groq LLM
                 │
                 ▼
         Generated Answer
```

---

# Project Structure

```text
.
├── Ingestion
│   ├── extract_pdf.py
│   ├── extract_txt.py
│   ├── ingestion.py
│   └── parser.py
│
├── models
│   ├── Chunking.py
│   ├── Embedding.py
│   ├── LLM.py
│   ├── reranker.py
│   └── vector_database.py
│
├── Retrieval
│   ├── query_processing.py
│   ├── Retrieval.py
│   └── retrieve.py
│
├── Pdfs
├── TextFiles
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# Technologies Used

- Python
- ChromaDB
- HuggingFace Embeddings
- BAAI/bge-m3
- BAAI/bge-reranker-base
- Groq API
- PyMuPDF
- pdf2image
- Tesseract OCR
- NLTK
- tiktoken
- PyTorch

---

# Installation

Clone the repository

```bash
git clone https://github.com/Avik3434/Intelligent-Document-Reviewer.git

cd Intelligent-Document-Reviewer
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the required dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Additional Requirements

OCR support requires the following external tools.

## Tesseract OCR

Install Tesseract OCR and update its executable path inside `extract_pdf.py`.

## Poppler

Install Poppler and configure its binary path inside `extract_pdf.py`.

These are only required when processing scanned PDF documents.

---

# Usage

Run the application

```bash
python main.py
```

The application allows you to:

- Index a new document
- Add additional documents
- Ask questions about indexed documents
- Exit the application

Example

```text
Question:

What is Retrieval-Augmented Generation?

Answer:

Retrieval-Augmented Generation (RAG) combines information retrieval with a language model by retrieving relevant document chunks before generating a grounded response.
```

---

# Retrieval Pipeline

The application follows a multi-stage retrieval pipeline.

```text
User Question
       │
       ▼
Generate Query Embedding
       │
       ▼
Semantic Search
(ChromaDB Top-K)
       │
       ▼
Cross-Encoder Reranker
       │
       ▼
Top Relevant Chunks
       │
       ▼
Prompt Construction
       │
       ▼
Groq LLM
       │
       ▼
Final Answer
```

---

# Supported File Types

| Format | Supported |
|---------|-----------|
| PDF | ✅ |
| TXT | ✅ |

---

# Current Workflow

1. Select a document
2. Extract text
3. Apply OCR if required
4. Generate metadata
5. Split the document into token-aware chunks
6. Generate dense embeddings
7. Store embeddings in ChromaDB
8. Ask a question
9. Retrieve the most relevant chunks
10. Rerank retrieved results
11. Generate a grounded response using the LLM

---

# Current Limitations

- Supports only PDF and TXT documents
- Command-line interface only
- OCR requires Tesseract and Poppler
- No conversation memory
- Designed for local execution

---

# Roadmap

## Version 1.2

- Hybrid retrieval (Dense + BM25)
- Metadata filtering
- Source citations
- Configurable retrieval settings
- Improved logging
- Better evaluation framework

## Future Versions

- Web interface (Streamlit/Gradio)
- Multi-user support
- Conversation history
- REST API
- Docker support
- Cloud deployment

---

# Why I Built This

I built this project to understand how Retrieval-Augmented Generation works beyond simply using existing libraries.

Instead of treating RAG as a black box, I wanted to explore each stage of the pipeline individually—from document extraction and OCR to chunking, embedding generation, vector search, reranking, and LLM integration.

The objective was not only to build a working application but also to gain practical experience with the concepts that power modern AI search systems.

---

# About the Author

Hi, I'm **Avik Mukherjee**, a Computer Science student from India with a strong interest in Artificial Intelligence, Machine Learning, Data Science, and Software Development.

I enjoy building projects from scratch to understand how systems work internally rather than relying solely on abstractions. This repository is part of my journey into Retrieval-Augmented Generation (RAG), semantic search, vector databases, and Large Language Models.

If you have suggestions, ideas, or feedback, feel free to open an issue or submit a pull request.
---

# License

This project is licensed under the MIT License.

---

# Version

## Current Version: **v1.1**

### What's New in v1.1

- Added TXT document support
- Improved token-aware chunking
- Migrated to **BAAI/bge-m3** embeddings
- Added Cross-Encoder reranking
- Improved retrieval accuracy
- Added duplicate document detection
- Enhanced metadata handling
- Refactored into a modular architecture
- Improved overall RAG pipeline performance and maintainability

Thank you