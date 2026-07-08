from vector_database import VectorStore
from ask_question import get_query_embedding

vectorstore = VectorStore()
def retrive(chunks):
    storage = vectorstore.store_chunks(chunks)
    if not storage:
        print("Storage failed!")

    print(vectorstore.collection.count())

    while True:
        question, query_vector = get_query_embedding()

        if query_vector is None:
            print("Goodbye!")
            break

        results = vectorstore.query(query_vector)

        for i, doc in enumerate(results["documents"][0], start=1):
            print(f"\nResult {i}")
            print(doc)
    return results["documents"], question