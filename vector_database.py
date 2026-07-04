import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
def store_chunks(chunks):
    try:
        collection = client.get_or_create_collection(name="document_chunks")

        texts = [chunk["text"] for chunk in chunks]

        embeddings = [chunk["embedding"] for chunk in chunks]

        ids = [str(chunk["chunk_id"]) for chunk in chunks]


        collection.add(documents = texts,
                    embeddings = embeddings,
                    ids = ids)
        print(f"Stored {len(chunks)} chunks successfully")
        return collection
    except Exception as e:
        print("Could not save in vector database", e)
        return None