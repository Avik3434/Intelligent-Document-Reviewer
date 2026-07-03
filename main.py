from chunking import Running
from extract import main_text
from list_pdfs import list_pdf

file_path = list_pdf()
text = main_text(file_path)
chunks = Running(text)