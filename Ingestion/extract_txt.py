"""
Plain text file extraction.

Extracts the full contents of a .txt file and wraps it in the same
list[dict] contract used by the PDF extractor. This allows .txt files
to flow through the chunking, embedding, and storage pipeline without
any changes to downstream functions.

Since text files have no page breaks, the entire file is treated as a
single "page" with page_number=0 and total_pages=1.
"""

from pathlib import Path
import hashlib

def extract_txt(file_path: str) -> dict:
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
    doc_id = hashlib.sha256(content.encode("utf-8")).hexdigest()

    document = {
        "metadata": {
            "source": path.name,
            "doc_id": doc_id,
            "total_pages": 1
        },
    
        "pages": [
            {
                "content": content,
                "metadata": {
                    "page_number": 0,
                    "extraction_method": "native",
                    }
                }
            ]
        } 

    return document
