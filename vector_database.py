import chromadb

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="document_chunks")
        
    def store_chunks(self, chunks: list) -> bool:
        try:
            texts = [chunk["text"] for chunk in chunks]
            embeddings = [chunk["embedding"] for chunk in chunks]
            ids = [str(chunk["chunk_id"]) for chunk in chunks]

            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                ids=ids,
            )
            print(f"Stored {len(chunks)} chunks successfully")
            return True         
        except Exception as e:
            print("Could not save in vector database", e)
            return False  
        
    def query(self, embedding,n_results=5):
        return self.collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )