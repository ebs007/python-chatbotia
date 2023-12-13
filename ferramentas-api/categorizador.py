# This code is for v1 of the openai package: pypi.org/project/openai
from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()

client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

def categorizaProduto(nome_do_produto, categorias_validas):
  # prompt_sistema = """
  # {str1}
  # {str2}
  # {str3}
  # {str4}
  # {str5}
  # """.format(
  #   str1='Você é um categorizador de produtos',
  #   str2='Você deve escolher uma categoria da lista abaixo:',
  #   # str3="""
  #   # ##### Lista de categoria válidas
  #   # Beleza
  #   # Entretenimento
  #   # Esportes
  #   # Outros
  #   # """,
  #   str3=categorias_validas,
  #   str3='Se as categorias informadas não forem categorias válidas, responda com "Não posso ajuda-lo com isso" e explique o motivo em detalhes.',
  #   str4="""
  #   ##### Exemplo
  #   Bola de tênis
  #   Esportes
  #   """,
  #   str5='O formato de saída deve ser apenas o nome da categoria'
  #   # str4=''
  #   # str1=''
  #   # str2=''
  #   # str3='',
  #   # str4=''
  # )

  prompt_sistema = f"""
  Você é um categorizador de produtos
  Você deve escolher uma categoria da lista abaixo:
  
  ##### Lista de categoria válidas
  {categorias_validas}
  ##### Exemplo
  Bola de tênis
  Esportes
  O formato de saída deve ser apenas o nome da categoria
  """

  resposta = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": prompt_sistema
      },
      {
        "role": "user",
        "content": nome_do_produto
      }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
  )
  print(resposta.choices[0].message.content)

# for i in range(0,5):
#   print(resposta.choices[i].message.content)
#   print('--------')

print('Digite as categorias validas:')
categorias_validas = input()
while True:
    print('Digite o nome do produto:')
    nome_do_produto = input()
    categorizaProduto(nome_do_produto, categorias_validas)