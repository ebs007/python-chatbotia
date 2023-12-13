from openai import OpenAI
import dotenv
import os
import json

dotenv.load_dotenv()

client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

resposta = client.chat.completions.create(model = 'gpt-3.5-turbo',
messages = [
    {
        'role': 'system',
        'content': 'Gere nomes de produtos fictícios sem descrição de acordo com a requisição do usuário'
    },
    {
        'role': 'user',
        'content': 'Gere 5 produtos'
    }
])

# jsonFormatado = json.dumps(resposta, indent=2)

print(resposta)