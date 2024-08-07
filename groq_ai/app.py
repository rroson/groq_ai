from dotenv import load_dotenv
import os
from groq import Groq
import time
import streamlit as st
import json
import random

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

st.title("Groq.ai")
pergunta = st.text_input("Escreva sua pergunta:")

def stream_data():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                # "content": "Como consigo os dados de todos os modelos de ia disponiveis no groq.ai?",
                "content": pergunta,
            }
        ],
        model="llama3-8b-8192",
    )

    for word in chat_completion.choices[0].message.content.split(" "):
        yield word + " "
        time.sleep(random.uniform(0.05, 0.2))
    
    atributos = {'Pergunta': pergunta}, {'Resposta': chat_completion.choices[0].message.content}

    with open("perguntas_respostas.json", "a") as f:
        for item in atributos:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


if st.button("Enviar"):
    st.write_stream(stream_data)

