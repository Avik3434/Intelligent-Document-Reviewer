import fitz  

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num, page in enumerate(doc):
        text = page.get_text()
        full_text += f"\n--- Page {page_num + 1} ---\n{text}"
    doc.close()
    return full_text

if __name__ == "__main__":
    text = extract_text("sample.pdf")
    print(text)
