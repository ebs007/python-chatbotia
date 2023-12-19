import openai
from openai import OpenAI
from datetime import datetime
import dotenv
import tiktoken
import time
import json

client = OpenAI()

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, 'w', encoding='utf8') as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f'Erro ao salvar arquivo: {e}')

def identifica_perfis(lista_de_compras_por_clientes):
  print('1. Iniciando identificação de perfis')
  prompt_sistema = """
  Identifique o perfil de compra para cada cliente a seguir.

  O formato de saída deve ser em JSON:

  cliente - descreva o perfil do cliente em 3 palavras

  {
    "clientes": [
        {
         "nome": "nome do cliente",
         "perfil": "descreva o perfil do cliente em 3 palavras"
        }
    ]
  }
  """

  resposta = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": lista_de_compras_por_clientes
            }
        ],
        )
  
  conteudo = resposta.choices[0].message.content
  json_resultado = json.loads(conteudo)
  print('Finalizou identificação do perfil')
  return json_resultado

def recomenda_produtos(perfil, lista_de_produtos):
  print('2. Inciando recomendação de produtos')
  prompt_sistema = f"""
  Você é um recomendador de produtos.
  Considere o seguinte perfil: {perfil}
  Recomende 3 produtos a partir da lista de produtos válidos e que seja adequados ao perfil informado.

  #### Lista de produtos válidos para recomendação
  {lista_de_produtos}

  A saída deve ser apenas o nome dos produtos recomendados em bullet points.
  """

  resposta = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            }
        ],
        )
  
  conteudo = resposta.choices[0].message.content
  print('2. Finalizando a recomendação de produtos')
  return conteudo 

def escreve_email(recomendações):
    print('3. Escrevendo email de recomendação')
    prompt_sistema = f"""
    Escreva um e-mail recomendando os seguintes produtos para um cliente:

    {recomendacoes}
    
    O e-mail deve ter no máximo 3 parágrafos.
    O tom deve ser amigável, informal e descontráido.
    Trate o cliente com alguém próximo e conhecido.
    """

    resposta = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                }
            ],
        )
  
    conteudo = resposta.choices[0].message.content
    print('3. Finalizando a escrita do e-mail')
    return conteudo 

lista_de_produtos = carrega('/home/erick/www/alura/python-chatbotia/ferramentas-api/dados/lista_de_produtos.txt')
lista_de_compras_por_clientes = carrega('/home/erick/www/alura/python-chatbotia/ferramentas-api/dados/lista_de_compras_10_clientes.csv')
perfis = identifica_perfis(lista_de_compras_por_clientes)
for cliente in perfis['clientes']:
    nome_do_cliente = cliente['nome']
    print(f'Inciando recomendação para o cliente {nome_do_cliente}')
    recomendacoes = recomenda_produtos(cliente['perfil'], lista_de_produtos)
    email = escreve_email(recomendacoes)
    salva(f'email-{nome_do_cliente}.txt', email)