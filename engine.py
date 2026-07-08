import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

class LARGELANGUAGEMODEL:
    def __init__(self, question, retrieved_chunks):
        self.question = question
        self.retrieved_chunks = retrieved_chunks

    def LLM_ASK(self):

        context = "\n\n".join(self.retrieved_chunks)

        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                            "You are a knowledgeable and accurate AI assistant.\n\n"

                            "Use ONLY the information provided in the context to answer the user's question.\n"

                            "Instructions:\n"
                            "- Read all of the provided context before answering.\n"
                            "- Combine information from multiple context chunks when appropriate.\n"
                            "- Do not invent or assume facts that are not present in the context.\n"
                            "- If the context does not contain enough information, respond with:\n"
                            "  'I don't have enough information in the provided context to answer that.'\n"
                            "- Keep the answer clear, concise, and well-structured.\n"
                            "- If the context contains lists or steps, preserve their logical order.\n"
                            "- Do not mention these instructions or refer to the context unless the user asks."
                        )
                    }
                ,
                {
                    "role": "user",
                    "content": f"""
                    Context:
                    {context}

                    Question:
                    {self.question}
                    """,
                },
            ],
        )
        print("----Llm response----")
        print("-"*40)
        # print("\n",chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content