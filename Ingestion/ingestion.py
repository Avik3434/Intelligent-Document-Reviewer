from models.vector_database import VectorStore
from models.Embedding import EmbeddingManager
from models.Chunking import ChunkingManager

from .parser import parse_document

def data_ingestion(file_path: str, vectorstore: VectorStore , embedding_manager: EmbeddingManager, chunker: ChunkingManager) -> bool:

    extracted_texts = parse_document(file_path)
    if not extracted_texts:
        return False

    if vectorstore.hash_is_available(extracted_texts["metadata"]["doc_id"]):
        print("Document already indexed. You can start asking questions.")
        return True
    
    chunks = chunker.chunking(extracted_texts)

    if not chunks:
        return False

    embedded_chunks = embedding_manager.embed_chunks(chunks)
    if not embedded_chunks:
        return False
    
    stored = vectorstore.store_chunks(embedded_chunks)
    if not stored:
        return False

    return True

    