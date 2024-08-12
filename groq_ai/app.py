from dotenv import load_dotenv
import os
import json
import time
import streamlit as st
from groq import Groq


if os.path.isfile('models.json'):
    try:
        # Carregue os dados do arquivo models.json
        with open('models.json') as f:
            data = json.load(f)

        # Crie um selectbox com as ids do json
        ids = [x['id'] for x in data['data']]
        id_selected = st.sidebar.selectbox("Selecione um ID", ids)

        # Encontre o modelo selecionado
        modelo_ia = next((x for x in data['data'] if x['id'] == id_selected), None)

        # Exiba os detalhes do modelo selecionado usando elementos markdown
        if modelo_ia:
            st.sidebar.markdown(f"Modelo: {modelo_ia['id']}")
            st.sidebar.markdown(f"Criado: {modelo_ia['created']}")
            st.sidebar.markdown(f"Por: {modelo_ia['owned_by']}")
            st.sidebar.markdown(f"Ativo: {modelo_ia['active']}")
            st.sidebar.markdown(f"Context window: {modelo_ia['context_window']}")
            st.sidebar.markdown(f"Public apps: {modelo_ia['public_apps']}")
        else:
            st.sidebar.write("ID não encontrado.")
    except json.JSONDecodeError as e:
        st.sidebar.error("Erro ao carregar o arquivo JSON: " + str(e))
else:
    modelo_ia = st.selectbox(
        "Selecione o Modelo de IA",
        (
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "llama3-groq-70b-8192-tool-use-preview",
            "gemma-7b-it",
        ),
    )

# Configuração de Streamlit
st.title("Groq.ai")
st.markdown(f"Criado por Ricardo Roson - Modelo: {modelo_ia['id']} - Escolha o modelo de IA na Sidebar.")

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
st.session_state.api_key = api_key

# Configuração inicial da chave da API
if 'api_key' not in st.session_state:
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            pass
    
    st.title("Configure a chave da API")
    api_key = st.text_input("Digite a chave da API (GROQ_API_KEY):")

    if st.button("Salvar"):
        with open('.env', 'w') as f:
            f.write(f"GROQ_API_KEY={api_key}")

        load_dotenv()
        st.session_state.api_key = api_key
        st.rerun()

    st.stop()

try:
    client = Groq(api_key=st.session_state.api_key)

    # Inicialização do histórico de conversas
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Função para gerar a resposta
    def get_response(user_input):
        # Preparar o histórico de mensagens para a API
        messages = [{"role": "user", "content": user_input}]
        # Adicionar mensagens anteriores ao histórico
        for msg in reversed(st.session_state.history):
            if msg["role"] == "ai":
                role = "assistant"
            else:
                role = "user"
            messages.insert(0, {"role": role, "content": msg["content"]})

        # Gerar a resposta da API Groq
        response = client.chat.completions.create(
            messages=messages,
            model=modelo_ia['id'],
        )
        return response.choices[0].message.content

    pergunta = st.chat_input("Escreva sua pergunta:")

    if pergunta:
        # Adicionar a pergunta do usuário ao histórico
        st.session_state.history.append({"role": "user", "content": pergunta})

        # Obter resposta do chatbot
        resposta = get_response(pergunta)

        # Adicionar a resposta do chatbot ao histórico
        st.session_state.history.append({"role": "ai", "content": resposta})

        # Exibir mensagens na tela
        for message in st.session_state.history:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "ai" else "👨"):
                st.write(message["content"])

        # Salvar as interações em arquivo
        pasta_interacoes = "interações"
        if not os.path.exists(pasta_interacoes):
            os.makedirs(pasta_interacoes)

        atributos = [{'Pergunta': pergunta}, {'Resposta': resposta}]
        arquivo = os.path.join(pasta_interacoes, "perguntas_respostas_{}.json".format(int(time.time())))
        with open(arquivo, "w") as f:
            f.writelines(json.dumps(atributos, ensure_ascii=False))

except Exception as e:
    st.error(f"Erro de autenticação: {e}")
    st.write("Verifique se a chave da API está correta e tente novamente.")
