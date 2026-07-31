from transformers import AutoTokenizer

class ChunkingManager:
    def __init__ (self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
        # self.vectordb = VectorStore()

    def chunking(self, documents: dict):
        if not documents:
            return []

        final_chunks = []

        steps = self.chunk_size - self.chunk_overlap
        global_chunk_index = 1
        metadata = documents["metadata"]
        for page in documents["pages"]:
            text = page["content"].strip()
            if not text:
                continue
            token_ids = self.tokenizer(text, add_special_tokens=False)["input_ids"]

            for i in range(0, len(token_ids), steps):
                chunk = self.tokenizer.decode(token_ids[i:i + self.chunk_size], skip_special_tokens = True)   

                doc_id = documents["metadata"]["doc_id"]
                source = documents['metadata']["source"]
                page_number = page["metadata"]["page_number"]
                chunk_id = f"{metadata['doc_id']}_{global_chunk_index}"

                final_chunks.append({
                    "content": chunk,
                    "metadata": {
                        "doc_id": doc_id,
                        "source": source,
                        "page_number": page_number,
                        "chunk_index": global_chunk_index,
                        "chunk_id": chunk_id
                    }
                })
                global_chunk_index += 1

        return final_chunks