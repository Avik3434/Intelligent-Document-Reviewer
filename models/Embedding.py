"""
Embedding generation using BGE-M3.

Provides a reusable embedding manager for generating dense vector embeddings
for both document chunks and user queries.
"""

from langchain_huggingface import HuggingFaceEmbeddings
import torch

class EmbeddingManager:
    """Wrapper around the BGE-M3 embedding model."""

    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={
                "device": "cuda" if torch.cuda.is_available() else "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True,
                "batch_size": 32,
            },
        )

    #Embeddings for actual chunks
    def embed_chunks(self, chunks: list) -> list:
        """
        Generate embeddings for all chunks and attach them in-place.

        Args:
            chunks: List of chunk dictionaries containing a "content" key.

        Returns:
            The same list with an "embedding" key added to each chunk.
        """
        if not chunks:
            raise ValueError("No chunks to embed.")

        texts = [chunk["content"] for chunk in chunks]
        embeddings = self.model.embed_documents(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        print(
            f"Embedded {len(chunks)} chunks | Dimension: {len(embeddings[0])}"
        )

        return chunks

    #Embeddings for the user query
    def embed_query(self, query: str) -> list[float]:
        """
        Generate an embedding for a user query.

        Args:
            query: User query text.

        Returns:
            Dense embedding vector.
        """
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        return self.model.embed_query(query)