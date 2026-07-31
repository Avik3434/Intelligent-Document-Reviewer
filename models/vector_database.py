import chromadb
from typing import Optional
COLLECTION_NAME = "document_chunks"

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        
    def store_chunks(self, chunks: list) -> int | bool:
        try:
            if not chunks:
                print("No chunks to store.")
                return False
            contents = [chunk["content"] for chunk in chunks]
            embeddings = [chunk["embedding"] for chunk in chunks]
            
            chunk_id = [chunk['metadata']['chunk_id'] for chunk in chunks]
            metadatas = [chunk['metadata'] for chunk in chunks]

            self.collection.add(
                documents=contents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=chunk_id,
            )
            
            print(f"Stored {len(chunks)} chunks successfully | Collection count {self.collection.count()}")
            return len(chunks)     
        except Exception as e:  
            raise RuntimeError("Failed to store chunks.") from e
            
        
    def query(self,query_embedding: list[float], n_results: int = 20, where_filter: Optional[dict] = None,) -> list[dict]:
        """
        Retrieve the most relevant chunks from the vector database.

        Args:
            embedding: Query embedding.
            n_results: Number of chunks to retrieve before reranking.
            where_filter: Optional metadata filter.

        Returns:
            A list of dictionaries containing the retrieved chunks.
        """
        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": n_results,
        }

        if where_filter is not None:
            kwargs["where"] = where_filter

        results = self.collection.query(**kwargs)

        retrieved_chunks = []
        if not results["documents"][0]:
            return []

        for doc, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved_chunks.append({
                "content": doc,
                "metadata": metadata,
                "distance": distance
            })
            
        return retrieved_chunks
    
    def count(self):
        return self.collection.count()

    def clear(self):
        """Wipe the collection for a fresh start."""
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.get_or_create_collection(name=self.collection.name)
        print("Collection cleared.")

    def hash_is_available(self, doc_id: str) -> bool:
        existing = self.collection.get(where={"doc_id": doc_id})
        if existing["ids"]:
            return True
        return False

