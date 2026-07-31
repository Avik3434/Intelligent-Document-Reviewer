from models.Embedding import EmbeddingManager

def _ask_question() -> str | None:
    """Prompt the user for a question. Returns the question or empty string on exit."""
    try:

        while True:
            question = input("Enter your question or type 'exit': ").strip()

            if question.lower() == "exit":
                return None

            if question:
                return question

            print("Please enter a valid question.")
                        
    except (KeyboardInterrupt, EOFError):
        return ""
    except Exception as e:
        print(f"Failed to read question: {e}")
        return None
    
#Gets the embedding of user query and returns both
def get_query_embeddings(embedding_manager: EmbeddingManager) ->(tuple[str, list[float]] | None):
    user_question = _ask_question()
    if not user_question:
        return None
    return user_question, embedding_manager.embed_query(user_question)