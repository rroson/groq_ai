from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "pergunte o que quiser aqui.",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)