import nltk
from nltk.tokenize import sent_tokenize
import tiktoken
# from extract import main_text

# Download sentence tokenizer
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# Use OpenAI's tokenizer (works for most models)
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    """Count tokens in text."""
    return len(tokenizer.encode(text))


def chunk_text(text, max_chunk_tokens=512, overlap_sentences=2):
    """
    Split text into sentence-aware chunks with token-based sizing.
    
    Args:
        text: Full extracted text
        max_chunk_tokens: Target tokens per chunk
        overlap_sentences: Number of sentences to overlap between chunks
    
    Returns:
        List of dicts with chunk text and metadata
    """
    sentences = sent_tokenize(text)
    chunks = []
    chunk_index = 0
    i = 0
    
    while i < len(sentences):
        current_chunk = ""
        chunk_start = i
        
        # Add sentences until we exceed max_chunk_tokens
        while i < len(sentences):
            test_chunk = current_chunk + " " + sentences[i]
            if count_tokens(test_chunk) < max_chunk_tokens:
                current_chunk = test_chunk
                i += 1
            else:
                break
        
        # If we only added one sentence and token count is huge, include it anyway
        if len(current_chunk) < 50 and i < len(sentences):
            current_chunk += " " + sentences[i]
            i += 1
        
        if current_chunk.strip():
            chunks.append({
                "chunk_id": chunk_index,
                "text": current_chunk.strip(),
                "tokens": count_tokens(current_chunk),
                "sentence_count": i - chunk_start
            })
            chunk_index += 1
        
        # Back up by overlap_sentences for next chunk
        i = max(chunk_start + 1, i - overlap_sentences)
    
    return chunks


def Running(text):
    chunks = chunk_text(text, max_chunk_tokens=50, overlap_sentences=2)

    for chunk in chunks:
        print(
            f"Chunk {chunk['chunk_id']}: "
            f"{chunk['tokens']} tokens, "
            f"{chunk['sentence_count']} sentences"
        )
        print(f"{chunk['text'][:80]}...\n")

    return chunks