from models.reranker import rerank
from .retrieve import retrieve
from models.LLM import LargeLanguageModel
from models.vector_database import VectorStore
from models.Embedding import EmbeddingManager

def data_retrieval(vectorstore: VectorStore, embedding_manager: EmbeddingManager):
    
    question, retrieved_query = retrieve(vectorstore, embedding_manager)

    if question is None:
        return None

    reranked_query = rerank(question, retrieved_query, top_k=5)
    print(f"\nQuestion: \"{question}\"")
    if not reranked_query:
        raise ValueError("Chunk could not be reranked")
    
    # print(reranked_query)
    llm_model = LargeLanguageModel(question, reranked_query)
    answer = llm_model.llm_response()

    return answer