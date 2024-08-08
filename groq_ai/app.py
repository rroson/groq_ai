from dotenv import load_dotenv
import os
import json
import time
import streamlit as st
from groq import Groq


st.title("Groq.ai")
st.markdown("Criado por Ricardo Roson")

if not load_dotenv():
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            pass
    
    st.title("Configure a chave da API")
    api_key = st.text_input("Digite a chave da API (GROQ_API_KEY):")

    if st.button("Salvar"):
        with open('.env', 'w') as f:
            f.write(f"GROQ_API_KEY={api_key}")

        load_dotenv()
        st.rerun()

    st.stop()

try:
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    pergunta = st.chat_input("Escreva sua pergunta:")

    buffer = []

    pasta_interacoes = "interações"
    if not os.path.exists(pasta_interacoes):
        os.makedirs(pasta_interacoes)

    def stream_data():
        global buffer

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": pergunta,
                }
            ],
            model = "llama-3.1-70b-versatile",
            # model = "mixtral-8x7b-32768",
            # model="llama3-8b-8192",
        )

        with st.chat_message("ai", avatar="🤖"):
            message = chat_completion.choices[0].message.content
            buffer.extend(message.split(" "))
            for word in buffer:
                yield word + " "
                time.sleep(0.05)
            buffer.clear()

        atributos = [{'Pergunta': pergunta}, {'Resposta': chat_completion.choices[0].message.content}]
        buffer.append(json.dumps(atributos, ensure_ascii=False))

    if pergunta:
        with st.chat_message("human", avatar="👨"):
            st.write(pergunta)

        st.write_stream(stream_data)

        arquivo = os.path.join(pasta_interacoes, "perguntas_respostas_{}.json".format(int(time.time())))
        with open(arquivo, "w") as f:
            f.writelines(buffer)

except Exception as e:
    st.error(f"Erro de autenticação: {e}")
    st.write("Verifique se a chave da API está correta e tente novamente.")

