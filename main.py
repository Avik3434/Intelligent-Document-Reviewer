"""
    Main entry point for the Intelligent Document Reviewer application.

    This module provides a simple command-line interface (CLI) that allows users to:

    - Ingest a document into the vector database.
    - Ask questions about the indexed documents using Retrieval-Augmented Generation (RAG).
    - Add additional documents to the existing knowledge base.
    - Exit the application.

    The application requires an initial document to be indexed before entering the
    main menu. Once indexed, users can repeatedly query the document collection or
    add more documents without restarting the program.
"""

import random
from pathlib import Path
from Ingestion.ingestion import data_ingestion
from Retrieval.Retrieval import data_retrieval
from models.vector_database import VectorStore
from models.Embedding import EmbeddingManager
from models.Chunking import ChunkingManager

#Use your own file path😊 
paths = ["Pdfs/Test.pdf", "TextFiles/RAG.txt"]

selected_path = random.choice(paths)
print(f"Testing: {Path(selected_path).name}")

vectorstore = VectorStore()
embedding_manager = EmbeddingManager()
chunker = ChunkingManager()

def main():
    while True:
        if data_ingestion(selected_path, vectorstore, embedding_manager, chunker):
            break
        print("Failed to load document. Try again.\n")

    # Main menu
    while True:
        print("\n===== Intelligent Document Reviewer =====")
        print("1. Ask questions")
        print("2. Add another document")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            answer = data_retrieval(vectorstore, embedding_manager)
            if answer is not None:
                print("Answer: \n")
                print(answer)

        elif choice == "2":
            data_ingestion(selected_path, vectorstore, embedding_manager, chunker)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")