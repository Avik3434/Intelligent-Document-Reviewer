"""
Embedding generation using BGE-M3.

Provides a pre-configured HuggingFace embedding model and a helper function
that generates dense vector embeddings for every chunk in the pipeline.
Embeddings are attached directly to each chunk dict, keeping content,
metadata, and vector in a single structure through to storage.
"""

from langchain_huggingface import HuggingFaceEmbeddings
import torch

# Pre-configured BGE-M3 embedding model.
# Uses GPU if available, normalizes output vectors, and processes 32 texts per batch.
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
    encode_kwargs={"normalize_embeddings": True, "batch_size": 32}
)


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Generate embeddings for all chunks and attach them in-place.

    Args:
        chunks: List of chunk dicts, each with a 'content' key.

    Returns:
        list[dict]: The same list with an 'embedding' key added to each dict.
                    Returns an empty list on failure.
    """
    if not chunks:
        raise ValueError("No chunks to embed")

    try:
        texts = [chunk["content"] for chunk in chunks]
        embedding_list = embeddings.embed_documents(texts)

        for chunk, embedding in zip(chunks, embedding_list):
            chunk["embedding"] = embedding

    except Exception as e:
        print(f"Embedding failed: {e}")
        return []

    print(f"Embedded {len(chunks)} chunks | Dimension: {len(embedding_list[0])}")
    return chunks