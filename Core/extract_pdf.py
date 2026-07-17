"""
PDF text extraction with OCR fallback and embedded image support.

This module extracts text from PDF files page-by-page. For each page, it
first attempts native text extraction. If the extracted text is shorter
than OCR_TEXT_THRESHOLD characters, the page is treated as a scanned image
and routed through Tesseract OCR. Optionally, large embedded images on
text-rich pages can also be OCR'd and appended to the page content.

All extracted pages share a single doc_id, making downstream metadata
filtering and document isolation straightforward.
"""

from pathlib import Path
import io
import fitz
import pytesseract
from PIL import Image
import uuid

# Pages with fewer native characters than this are treated as scanned.
OCR_TEXT_THRESHOLD = 20

# Resolution multiplier for OCR page rendering. Higher = more accurate, slower.
OCR_ZOOM = 2.0

# Embedded images smaller than this (in pixels, either dimension) are skipped.
# Filters out logos, bullet icons, and decorative dividers.
MIN_EMBEDDED_IMAGE_DIM = 100


def _ocr_page(doc: fitz.Document, page_number: int) -> str:
    """Render a single page as an image and extract text via Tesseract OCR."""
    try:
        page = doc.load_page(page_number)
        matrix = fitz.Matrix(OCR_ZOOM, OCR_ZOOM)
        pix = page.get_pixmap(matrix=matrix)
        image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        return pytesseract.image_to_string(image).strip()
    except:
        raise ValueError("Page could not be loaded")


def _extract_embedded_images(doc: fitz.Document, page_number: int) -> list[str]:
    """Extract text from large embedded images on a page. Skips small logos/icons."""
    page = doc.load_page(page_number)
    texts = []

    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        pil_image = Image.open(io.BytesIO(image_bytes))

        if pil_image.width < MIN_EMBEDDED_IMAGE_DIM or pil_image.height < MIN_EMBEDDED_IMAGE_DIM:
            continue

        ocr_text = pytesseract.image_to_string(pil_image).strip()
        if ocr_text:
            texts.append(ocr_text)

    return texts


def extract_text(
    pdf_path: str,
    ocr_threshold: int = OCR_TEXT_THRESHOLD,
    extract_embedded_images: bool = False
) -> list[dict]:
    """Extract text from a PDF file page-by-page.

    Args:
        pdf_path: Path to the PDF file.
        ocr_threshold: Minimum native text length before OCR fallback kicks in.
        extract_embedded_images: If True, OCR large embedded images on text-rich pages.

    Returns:
        list[dict]: One dict per page with keys:
            - 'content' (str): The extracted text.
            - 'metadata' (dict): source, doc_id, page_number, total_pages, extraction_method.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    try:
        doc = fitz.open(str(path))
        doc_id = str(uuid.uuid4())
        total_pages = len(doc)
        extracted_pages = []

        for page_number in range(total_pages):
            page = doc.load_page(page_number)
            native_text = page.get_text().strip()

            if len(native_text) < ocr_threshold:
                content = _ocr_page(doc, page_number)
                extraction_method = "ocr"
            else:
                content = native_text
                extraction_method = "native"

                if extract_embedded_images:
                    image_texts = _extract_embedded_images(doc, page_number)
                    if image_texts:
                        content += "\n\n" + "\n\n".join(image_texts)
                        extraction_method = "native+ocr_images"

            extracted_pages.append({
                "content": content,
                "metadata": {
                    "source": path.name,
                    "doc_id": doc_id,
                    "page_number": page_number,
                    "total_pages": total_pages,
                    "extraction_method": extraction_method
                }
            })
    finally:
        doc.close()

    return extracted_pages


if __name__ == "__main__":
    pages = extract_text("Pdfs/Fruits.pdf")
    for p in pages[:3]:
        print(f"Page {p['metadata']['page_number']} | Method: {p['metadata']['extraction_method']}")
        print(f"doc id: {p['metadata']['doc_id']} | total pages: {p['metadata']['total_pages']}")
        print(p['content'][:100])
        print("---")