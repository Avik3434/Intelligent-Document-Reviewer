from chunking import final_running
from extract import main_text
from list_pdfs import list_pdf
from embedding import embed_chunks
from vector_database import store_chunks


# Currently this is only available for PDF. later more things will be implemented.


file_path = list_pdf()
text = main_text(file_path)
chunks = final_running(text)
embedded_chunks = embed_chunks(chunks)
storage = store_chunks(embedded_chunks)

if storage is None:
    print("Storage failed!")
