from embedding import embed_query

def ask_question():
    """Asks question from the user and retrive the data from the vector database"""
    while True:
        try:
            user_question = input("\n\nAsk a question below (or type 'exit'): ").strip()

            if user_question.lower() == 'exit':
                return None
            
            if not user_question:
                print("Enter a valid question!")
                continue

            print("question accepted")
            return user_question
        except Exception as e:
            print(f"Error: {e}")    

def get_query_embedding():
    user_question = ask_question()
    if not user_question:
        print("No question is entered!")
        return None
    return user_question, embed_query(user_question)