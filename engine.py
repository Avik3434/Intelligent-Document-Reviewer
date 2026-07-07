import os
from dotenv import load_dotenv
from groq import Groq
# Load variables from .env file into environment
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

ask = input("Enter a question: ")
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{ask}",
        }
    ],
    model="openai/gpt-oss-120b",
)

print(chat_completion.choices[0].message.content)