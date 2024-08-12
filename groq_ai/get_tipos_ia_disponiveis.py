'''
Esses são modelos do tipo chat e áudio e são diretamente acessíveis por meio do
endpoint da API de modelos do GroqCloud usando os IDs de modelo disponíveis.
Você pode usar o endpoint https://api.groq.com/openai/v1/models para retornar uma
lista JSON de todos os modelos ativos:
'''
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

# Salva o JSON corretamente no arquivo
with open("models.json", "w") as f:
    json.dump(response.json(), f, indent=4)  # Usa json.dump para garantir que o JSON esteja formatado corretamente
