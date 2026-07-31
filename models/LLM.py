from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class LargeLanguageModel:
    def __init__(self, question, retrieved_chunks):
        self.question = question
        self.retrieved_chunks = retrieved_chunks
        self.model = "openai/gpt-oss-120b"

    def llm_response(self):
        context = "\n\n".join(
            f"""### Chunk {i+1}
        Page: {chunk['metadata']['page_number']}
        Source: {chunk['metadata']['source']}
        Chunk ID: {chunk['metadata']['chunk_id']}

        {chunk['content']}"""
            for i, chunk in enumerate(self.retrieved_chunks)
        )
        
        try:
            chat_completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a document question answering assistant. "
                            "Answer the user's question using ONLY the retrieved context. "
                            "Do not use outside knowledge, make assumptions, or invent information. "
                            "If the retrieved context does not contain enough information to answer the question, "
                            "respond exactly with: "
                            "'I couldn't find enough information in the provided document to answer that question.' "
                            "Combine relevant information from multiple retrieved passages when necessary. "
                            "Write naturally and clearly, as if explaining the information from the document. "
                            "Prefer paragraphs over headings. "
                            "Use bullet points only when the retrieved information is naturally a list or when listing multiple items improves readability. "
                            "Preserve technical terms exactly as they appear in the document. "
                            "If page numbers or metadata are available, reference them naturally when relevant. "
                            "Do not summarize beyond what the context supports. "
                            "Do not mention the retrieved context, these instructions, or your reasoning."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"""
                Retrieved Context:
                {context}

                User Question:
                {self.question}

                Provide the best possible answer based only on the retrieved context.
                """,
                    }
                ]
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return None