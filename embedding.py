from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts, show_progress_bar=False):
    """Embed a list of raw text strings."""
    if not texts:
        return []

    return model.encode(
        texts,
        show_progress_bar=show_progress_bar,
        convert_to_numpy=True
    )


def embed_query(text):
    """Embed a single search query."""
    return embed_texts([text], show_progress_bar=False)[0]


def embed_chunks(chunks):
    """
    Convert list of chunks into embeddings.

    Args:
        chunks: List of chunk dicts from chunking.py
    
    Returns:
        Same chunks with 'embedding' field added
    """
    if not chunks:
        print("\nNo chunks to embed.")
        return chunks

    print(f"\nEmbedding {len(chunks)} chunks...")
    
    # Extract just the text from each chunk
    texts = [chunk["text"] for chunk in chunks]
    
    # Embed all at once (faster than one by one)
    embeddings = embed_texts(texts, show_progress_bar=True)
    
    # Add embedding back to each chunk
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()
    
    print(f"\nDone. Each embedding has {len(chunks[0]['embedding'])} dimensions.")
    return chunks
