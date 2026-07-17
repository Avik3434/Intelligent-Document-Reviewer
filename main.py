"""
End-to-end ingestion and query pipeline for v1.1.

This script demonstrates the complete RAG ingestion workflow:
    1. Clear the vector store (development safety net).
    2. Extract text from a PDF or TXT file.
    3. Split the extracted pages into overlapping chunks.
    4. Generate dense embeddings for each chunk.
    5. Store chunks, metadata, and embeddings in Chroma.
    6. Run a test query with a metadata filter to verify document isolation.

The pipeline uses a shared contract (list[dict]) across all stages,
allowing any supported file type to flow through the same path without
modification to downstream functions.
"""

from config import *

vectorstore = VectorStore()

# ── Step 1: Clear any old data (dev safety) ──
# Wipes the collection so repeated test runs start from a clean slate.
# This is a development utility; never call it on a user action in production.
vectorstore.clear()

# ── Step 2: Extract ──
# Extracts text page-by-page from the given file. Returns a list of dicts,
# each with 'content' and 'metadata' keys. Metadata includes source filename,
# a unique doc_id, page number, total pages, and extraction method used.
pages = extract_text("Pdfs/Fruits.pdf")
print(f"Extracted {len(pages)} pages")

# ── Step 3: Chunk ──
# Splits each page into smaller, overlapping chunks using recursive character
# splitting. Each chunk inherits the page's metadata and receives a unique
# chunk_id and chunk_index. Tiny orphan chunks (< 100 chars) are merged into
# the previous chunk to avoid semantically empty fragments.
chunks = chunk_pages(pages)
print(f"Chunked into {len(chunks)} chunks")

# ── Step 4: Embed ──
# Generates dense vector embeddings for every chunk using the BGE-M3 model.
# Embeddings are attached directly to each chunk dict under the 'embedding'
# key. The enriched chunks list is returned for handoff to the vector store.
chunks = embed_chunks(chunks)

# ── Step 5: Store ──
# Persists all chunks—content, metadata, and pre-computed embeddings—into
# the Chroma vector database. Metadata is stored alongside each vector to
# enable filtered queries (e.g., scoping retrieval to a single document).
vectorstore.store_chunks(chunks)

# ── Step 6: Test query ──
# Retrieves the doc_id from the first chunk (all chunks share the same one)
# and runs a semantic search scoped exclusively to that document. The where
# filter proves that no chunks from other PDFs leak into the results.
doc_id = chunks[0]["metadata"]["doc_id"]
query_text = "Which fruit is better in vitamin C?"
query_embedding = embeddings.embed_query(query_text)

results = vectorstore.query(
    query_embedding,
    where_filter={"doc_id": doc_id}
)

print(f"\n── Query: '{query_text}' ──")
print(f"Filtered by doc_id: {doc_id}\n")

for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    print(f"Chunk {i+1} | Section: {meta.get('section_title', 'N/A')} | Page: {meta['page_number']}")
    print(f"{doc[:50]}...")
    print()

print(f"Total chunks in collection: {vectorstore.count()}")