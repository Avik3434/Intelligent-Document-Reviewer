from chunking import final_running
from extract import main_text
from list_pdfs import list_pdf
from embedding import embed_chunks
from vector_database import VectorStore
from ask_question import get_query_embedding
# from trial import Chunking
# from BetterChunking import chunk_by_coherence

# Currently this is only available for PDF. later more things will be 
vector_store = VectorStore()


file_path = list_pdf()
text = main_text(file_path)
chunks = final_running(text)
# chunks = Chunking(text)
# chunks = chunk_by_coherence(text)
embedded_chunks = embed_chunks(chunks)

storage = vector_store.store_chunks(embedded_chunks)
if not storage:
    print("Storage failed!")

print(vector_store.collection.count())


while True:
    question, query_vector = get_query_embedding()

    if query_vector is None:
        print("Goodbye!")
        break

    results = vector_store.query(query_vector)

    for i, doc in enumerate(results["documents"][0], start=1):
        print(f"\nResult {i}")
        print(doc)