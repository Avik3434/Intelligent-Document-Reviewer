from chunking import final_running
from extract import main_text
from list_pdfs import list_pdf
from embedding import embed_chunks
from vector_database import VectorStore
from ask_question import get_query_embedding
from retrival import retrive
from engine import LARGELANGUAGEMODEL
from ask_question import ask_question

# Currently this is only available for PDF. later more things will be 
vector_store = VectorStore()

file_path = list_pdf()
text = main_text(file_path)
chunks = final_running(text)
embedded_chunks = embed_chunks(chunks)
# question = ask_question()

# retrive = retrive(embedded_chunks)
storage = vector_store.store_chunks(chunks)
if not storage:
    print("Storage failed!")

print(vector_store.collection.count())

question, query_vector = get_query_embedding()

if query_vector is None:
    print("Goodbye!")

results = vector_store.query(query_vector)

for i, doc in enumerate(results["documents"][0], start=1):
    print(f"\nResult {i}")
    print(doc)
if not results["documents"][0]:
    print("No relevant information found")
    
LLM = LARGELANGUAGEMODEL(question, results["documents"][0])
llm = LLM.LLM_ASK()
print(llm)
