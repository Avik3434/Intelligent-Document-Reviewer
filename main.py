from chunking import final_running
from extract import main_text
from list_pdfs import list_pdf
# Currently this is only available for PDF. later more things will be implemented.

file_path = list_pdf()
text = main_text(file_path)
chunks = final_running(text)  