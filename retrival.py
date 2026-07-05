import chromadb

Client = chromadb.PersistentClient(path="./chroma_db")
collection = Client.get_or_create_collection("document_chunks")

def search_database(embedding,n_results=5):
    return collection.query(
    query_embeddings=[embedding],
    n_results=n_results
)