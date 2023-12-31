from openai import OpenAI
from datetime import datetime
import dotenv
import tiktoken

print(datetime.now())

dotenv.load_dotenv()
client = OpenAI()

codificador = tiktoken.encoding_for_model('gpt-3.5-turbo')

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")


prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("/home/erick/www/alura/python-chatbotia/ferramentas-api/dados/lista_de_compras_100_clientes.csv")

# print(f'{prompt_usuario}')

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)

print(f'Número de tokens na entrada: {numero_de_tokens}')

modelo = 'gpt-3.5-turbo'

tamanho_esperado_saida = 2048

if(numero_de_tokens >= 4096 - tamanho_esperado_saida):
  modelo = 'gpt-3.5-turbo-16k'

print(f'Modelo escolhido: {modelo}')

resposta = client.chat.completions.create(
  model=modelo,
  messages=[
    {
      "role": "system",
      "content": prompt_sistema
    },
    {
      "role": "user",
      "content": prompt_usuario
    }
  ],
  temperature=1,
  max_tokens=tamanho_esperado_saida,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(resposta.choices[0].message.content)

print(datetime.now())