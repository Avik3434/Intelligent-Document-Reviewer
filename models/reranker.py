from sentence_transformers import CrossEncoder

model = CrossEncoder("BAAI/bge-reranker-base")

def rerank(query: str, chunks: list[dict], top_k: int) -> list[dict]:
    if not chunks:
        return []

    pairs = [[query, chunk["content"]] for chunk in chunks]

    scores = model.predict(
        pairs,
        batch_size=16,
        show_progress_bar=False
    )

    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    ranked_chunks = sorted(chunks, key=lambda chunk: chunk["rerank_score"] , reverse=True)

    unique_chunks = []
    seen = set()


    for chunk in ranked_chunks:
        chunk_id = chunk['metadata']['chunk_id']

        if chunk_id not in seen:
            seen.add(chunk_id)
            unique_chunks.append(chunk)

    return unique_chunks[:top_k]