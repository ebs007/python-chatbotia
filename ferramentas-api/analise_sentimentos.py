import openai
from openai import OpenAI
from datetime import datetime
import dotenv
import tiktoken
import time

print(datetime.now())

dotenv.load_dotenv()
client = OpenAI()

codificador = tiktoken.encoding_for_model('gpt-3.5-turbo')

def analise_sentimento(nome_do_produto):
    # nome_do_produto = 'Tapete de yoga'

    prompt_sistema = """
    Você é um analisador de sentimentos de avaliações de produtos.
    Escreva um parágrafo com até 50 palavras resumindo as avaliações e depois atribua qual o sentimento geral para o produto.
    Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

    #### Formato de saída
    Nome do produto:
    Resumo das avaliações:
    Sentimento geral: [aqui deve ser POSITIVO, NEUTRO ou NEGATIVO]
    Pontos fortes: [3 bullet points]
    Pontos fracos: [3 bullet points]
    """

    prompt_usuario = carrega(f"/home/erick/www/alura/python-chatbotia/ferramentas-api/dados/avaliacoes-{nome_do_produto}.txt")
    print(f'Iniciando a análise deo produto: {nome_do_produto}')

    # print(f'{prompt_usuario}')

    lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
    numero_de_tokens = len(lista_de_tokens)

    print(f'Número de tokens na entrada: {numero_de_tokens}')

    modelo = 'gpt-3.5-turbo'

    tamanho_esperado_saida = 2048
    tempo_de_espera = 5

    if(numero_de_tokens >= 4096 - tamanho_esperado_saida):
      modelo = 'gpt-3.5-turbo-16k'

    print(f'Modelo escolhido: {modelo}')

    tentativas = 0

    while tentativas < 3:
        
      tentativas += 1

      print(f'Tentativa {tentativas}')

      try:
        # raise openai.APIError
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

        # print(resposta.choices[0].message.content)

        salva(f'/home/erick/www/alura/python-chatbotia/ferramentas-api/dados/analise-{nome_do_produto}', resposta.choices[0].message.content)

        print('Analise concluída com sucesso!')
        print(datetime.now())
        return
      
      except openai.AuthenticationError as e:
        print(f'Erro de autenticacao: {e}')
      
      except openai.RateLimitError as e:
        print(f'Erro de limite de taxa: {e}')
        time.sleep(tempo_de_espera)
        tempo_de_espera *= 2
      except openai.APIError as e:
        print(f'Erro de API: {e}')
        time.sleep(5)

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

lista_de_produtos = ['Tapete de yoga', 'Tabuleiro de xadrez de madeira']
for nome_produto in lista_de_produtos:
    analise_sentimento(nome_produto)
