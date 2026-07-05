from chunking import final_running
from extract import main_text
from list_pdfs import list_pdf
from embedding import embed_chunks
from vector_database import VectorStore
from ask_question import get_query_embedding

# Currently this is only available for PDF. later more things will be implemented.

# Creating vectorstore object
vector_store = VectorStore()

# ----RAG Pipeline---
# getting file -> extract text -> make chunks -> embedding

file_path = list_pdf()
text = main_text(file_path)
chunks = final_running(text)
embedded_chunks = embed_chunks(chunks)

# store embedding chunks in vector database

storage = vector_store.store_chunks(embedded_chunks)
if not storage:
    print("Storage failed!")

# asks user question -> embedding -> retrival
while True:
    question, query_vector = get_query_embedding()

    if query_vector is None:
        print("Goodbye!")
        break

    results = vector_store.query(query_vector)

    for i, doc in enumerate(results["documents"][0], start=1):
        print(f"\nResult {i}")
        print(doc)