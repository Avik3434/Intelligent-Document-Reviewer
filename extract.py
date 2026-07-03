import fitz
import pytesseract
import os
from pdf2image import convert_from_path
from list_pdfs import list_pdf
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract\tessdata"
POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num, page in enumerate(doc):
        text = page.get_text().strip()
         
        # Check if extracted text is empty or looks corrupted
        if not text or looks_corrupted(text):
            print(f"Page {page_num + 1}: Using OCR")
            text = ocr_page(pdf_path, page_num)
        else:
            print(f"Page {page_num + 1}: Using embedded text")
        
        full_text += f"\n--- Page {page_num + 1} ---\n{text}"

    doc.close()
    return full_text

def looks_corrupted(text):
    """Check if extracted text appears to be garbled/corrupted."""
    if not text:
        return True
    
    # Count non-ASCII characters
    non_ascii = sum(1 for c in text if ord(c) > 127)
    ascii_count = len(text)
    
    # If more than 30% of characters are non-ASCII/unusual, likely corrupted
    if ascii_count > 0 and (non_ascii / ascii_count) > 0.3:
        return True
    
    return False

def ocr_page(pdf_path, page_num):
    images = convert_from_path(
        pdf_path,
        first_page=page_num + 1,
        last_page=page_num + 1,
        poppler_path=POPPLER_PATH
    )
    ocr_text = pytesseract.image_to_string(images[0])
    return ocr_text

def main_text(pdf_path):
    return extract_text(pdf_path)
    

# if __name__ == "__main__":
#     text = extract_text("sample.pdf")
#     print(text)