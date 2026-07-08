# RAG PDF Question Answering System

A simple Retrieval-Augmented Generation (RAG) application that allows you to ask questions about PDF documents.

The project extracts text from PDF files, intelligently splits the content into chunks, generates semantic embeddings, stores them in a vector database, retrieves the most relevant information for a query, and finally uses an LLM to generate an answer based only on the retrieved context.

This project was built as a learning project to understand how a complete RAG pipeline works from scratch without relying heavily on high-level frameworks.

---

## Features

* PDF text extraction
* OCR fallback for scanned PDFs
* Token-aware chunking
* Sentence Transformer embeddings
* ChromaDB vector database
* Semantic similarity search
* LLM-powered question answering
* Modular code structure

---

## Pipeline

```text
PDF
 │
 ▼
Text Extraction
 │
 ▼
Chunking
 │
 ▼
Embedding
 │
 ▼
ChromaDB
 │
 ▼
Semantic Retrieval
 │
 ▼
LLM
 │
 ▼
Answer
```

---

## Project Structure

```
.
.
├── ask_question.py
├── chunking.py
├── embedding.py
├── engine.py
├── extract.py
├── list_pdfs.py
├── main.py
├── retrival.py
├── vector_database.py
├── requirements.txt
└── README.md
```

---

## Technologies Used

* Python
* ChromaDB
* Sentence Transformers
* PyMuPDF
* Tesseract OCR
* pdf2image
* NLTK
* Groq API

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

---

## Additional Requirements

This project also requires two external tools.

### Tesseract OCR

Install Tesseract OCR and update the path in `extract.py`.

### Poppler

Install Poppler and update the Poppler path in `extract.py`.

These are only required for OCR support when processing scanned PDF documents.

---

## Usage

Place your PDF files in any directory and update the path in `list_pdfs.py` to point to that location.

Run the application.

```bash
python main.py
```

Choose a PDF from the list.

After indexing is complete, ask questions about the document.

Example:

```
Ask a question:

> What is Retrieval-Augmented Generation?

Answer:

Retrieval-Augmented Generation (RAG) combines information retrieval with a language model to answer questions using relevant context extracted from documents.
```

---

## Current Workflow

1. Select a PDF
2. Extract text
3. Perform OCR if necessary
4. Split the document into chunks
5. Generate embeddings
6. Store embeddings in ChromaDB
7. Ask a question
8. Retrieve the most relevant chunks
9. Generate the final answer using the LLM

---

## Limitations

* Supports PDF documents only.
* Indexes one document at a time.
* Requires manual installation of Tesseract and Poppler.
* Currently uses a command-line interface.

---

## Future Improvements

* Support multiple document formats
* Batch indexing
* Metadata-based retrieval
* Hybrid search
* Cross-encoder reranking
* Web interface
* Streaming responses
* Docker support
* Better configuration management

---

## Why I Built This

I built this project to gain a deeper understanding of Retrieval-Augmented Generation by implementing the complete pipeline from scratch. Rather than relying heavily on high-level frameworks, I wanted to understand how each stage—document extraction, chunking, embedding generation, vector search, retrieval, and answer generation—works together to produce accurate responses.

## License

This project is available under the MIT License.
 
## About the Author

Hi, I'm **Avik Mukherjee**, a Computer Science student from India with a strong interest in Artificial Intelligence, Machine Learning, and Software Development.

I enjoy building projects from the ground up to understand how they work internally rather than relying solely on high-level frameworks. This repository is part of my learning journey as I explore Retrieval-Augmented Generation (RAG), vector databases, embeddings, and large language models.

I'm continuously working on improving this project and welcome feedback, suggestions, and contributions.

## Version

**Current Version:** v1.0

This release implements a complete end-to-end RAG pipeline for PDF-based question answering using semantic retrieval and a large language model.