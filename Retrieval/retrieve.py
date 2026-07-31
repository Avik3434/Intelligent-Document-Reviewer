from .query_processor import get_query_embeddings
from models.vector_database import VectorStore
from models.Embedding import EmbeddingManager

def retrieve(vectorstore: VectorStore, embedding_manager: EmbeddingManager):
    query_data = get_query_embeddings(embedding_manager)
    if query_data is None:
        return None

    user_question, query_embedding = query_data
    retrieved_chunks = vectorstore.query(query_embedding)
    
    return user_question, retrieved_chunks