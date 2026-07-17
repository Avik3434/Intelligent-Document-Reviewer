import chromadb

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="document_chunks")
        
    def store_chunks(self, chunks: list) -> bool:
        try:
            content = [chunk["content"] for chunk in chunks]
            embeddings = [chunk["embedding"] for chunk in chunks]
            chunk_id = [str(chunk['metadata']['chunk_id']) for chunk in chunks]
            metadatas = [chunk['metadata'] for chunk in chunks]

            self.collection.add(
                documents=content,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=chunk_id,
            )
            print(f"Stored {len(chunks)} chunks successfully | Collection count {self.collection.count()}")
            return True         
        except Exception as e:
            print("Could not save in vector database", e)
            return False  
        
    def query(self, embedding, n_results=5, where_filter = None):
        """Query with optional metadata filtering"""
        kwargs = {
            "query_embeddings": [embedding],
            "n_results": n_results,
        }
        if where_filter:
            kwargs["where"] = where_filter
        
        return self.collection.query(**kwargs)
    
    def count(self):
        return self.collection.count()
    

    def clear(self):
        """Wipe the collection for a fresh start."""
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.get_or_create_collection(name=self.collection.name)
        print("Collection cleared.")