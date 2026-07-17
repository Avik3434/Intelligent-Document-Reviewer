from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_pages(pages: list[dict], chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
    """Split extracted pages into chunks. Each chunk inherits page metadata
    and gets a unique chunk_id and chunk_index."""
    
    if not pages:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    final_chunks = []
    global_chunk_index = 0
    doc_id = pages[0]["metadata"]["doc_id"]
    
    for page in pages:
        page_text = page["content"]
        page_metadata = page["metadata"]
        raw_chunks = text_splitter.split_text(page_text)
        
        for chunk_text in raw_chunks:
            if not chunk_text.strip():
                continue
            
            # Merge tiny orphan chunks into the previous chunk
            if len(chunk_text) < 100 and final_chunks:
                final_chunks[-1]["content"] += "\n" + chunk_text
                continue
            
            chunk_metadata = {
                **page_metadata,
                "chunk_id": f"{doc_id}_chunk_{global_chunk_index:04d}",
                "chunk_index": global_chunk_index,
            }
            
            final_chunks.append({
                "content": chunk_text,
                "metadata": chunk_metadata
            })
            
            global_chunk_index += 1
    
    return final_chunks