from pathlib import Path

from .extract_pdf import extract_pdf
from .extract_txt import extract_txt

def parse_document(file_path: str) -> dict:
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return extract_pdf(file_path)

    elif suffix == ".txt":
        return extract_txt(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")
