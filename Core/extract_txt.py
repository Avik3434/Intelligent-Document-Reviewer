"""
Plain text file extraction.

Extracts the full contents of a .txt file and wraps it in the same
list[dict] contract used by the PDF extractor. This allows .txt files
to flow through the chunking, embedding, and storage pipeline without
any changes to downstream functions.

Since text files have no page breaks, the entire file is treated as a
single "page" with page_number=0 and total_pages=1.
"""

import uuid
from pathlib import Path


def extract_txt(file_path: str) -> list[dict]:
    """Extract text from a plain text file.

    Args:
        file_path: Path to the .txt file.

    Returns:
        list[dict]: Single-element list with keys:
            - 'content' (str): The full file contents.
            - 'metadata' (dict): source, doc_id, page_number, total_pages, extraction_method.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = path.read_text(encoding="utf-8")
    doc_id = str(uuid.uuid4())

    return [{
        "content": content,
        "metadata": {
            "source": path.name,
            "doc_id": doc_id,
            "page_number": 0,      # Text files have no page breaks
            "total_pages": 1,
            "extraction_method": "native",
        }
    }]


if __name__ == "__main__":
    texts = extract_txt("../TextFiles/RAG.txt")
    for text in texts:
        print(f"Source: {text['metadata']['source']} | Doc id: {text['metadata']['doc_id']} ")
        print(f"Extraction method: {text['metadata']['extraction_method']}")
        print(f"Content: \n{text['content'][:200]}")
        print("-" * 40)