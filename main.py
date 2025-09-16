import requests
from bs4 import BeautifulSoup
import sqlite3 as s

from create_database import *
from database import verifica_se_o_produto_existe, atualizar_produto, inserir_registro
from product import Product

headers = {'User-Agent': 'Mozilla/5.0...'}
conexao = s.connect('web_scraping_database.db')
cursor = conexao.cursor()
criar_tabela(conexao, cursor)

def busca_informacoes_redirecionamento(lista_de_atributos):
    informacoes_tecnicas = ""
    if lista_de_atributos is None:
        return "Esse produto não possui informações técnicas."

    for elementos in lista_de_atributos:
        for item in elementos:
              itens_nomes = item.find('td', class_='attribute-name').text
              itens_valores = item.find('td', class_='attribute-value').text
              informacoes_tecnicas = informacoes_tecnicas + itens_nomes +  " | "  + itens_valores + "\n"

    return informacoes_tecnicas

def pega_dados_da_url(url, parametro_pesquisa_usuario, opcao_digitada):
 try:
     html = requests.get(url, headers=headers, timeout=10).content
     soup = BeautifulSoup(html, 'html.parser')
     elementos_da_lista = soup.find_all('div', class_='product-list-info')
     elementos_com_id = soup.find_all('div', class_='product-list-image-container', id=True)
     sku_produto = soup.find_all('div', class_=['product', 'product tag-atualizacao-uoou'])
     lista_de_produtos = []
     for i, elementos_da_lista in enumerate(elementos_da_lista):
         titulo = elementos_da_lista.find('h4', class_='product-list-name').text
         preco = elementos_da_lista.find('span', class_='to-price').text
         valor_parcela = elementos_da_lista.find('span', class_='installments-amount').text
         numero_parcelas = elementos_da_lista.find('span', class_='installments-number').text
         preco_pix = elementos_da_lista.find('div', class_='cash-payment-container').text
         url_direcionamento = elementos_com_id[i].get('id')
         url_do_produto = "https://www.lojamaeto.com/" + url_direcionamento
         html = requests.get(url_do_produto).content
         soup_novo_html = BeautifulSoup(html, 'html.parser')
         atributos = soup_novo_html.find('table', class_='table table-striped table-hover')
         informacoes_tecnicas = busca_informacoes_redirecionamento(atributos)
         product = Product(sku_produto[i].get('data-sku'), titulo, preco.replace(",",".").replace("R$ ", ""), preco_pix.replace("no pix", "").replace(",",".").replace("R$ ", ""), valor_parcela.replace(",",".").replace("R$ ", ""), numero_parcelas.replace("x", ""), informacoes_tecnicas)
         lista_de_produtos.append(product)

     for item in lista_de_produtos:
        filtro_encontrado = False

        match int(opcao_digitada):
            case 1:
                if item.sku == parametro_pesquisa_usuario:
                    filtro_encontrado = True
            case 2:
                if item.titulo.__contains__(parametro_pesquisa_usuario):
                    filtro_encontrado = True
            case 3:
                if item.preco == parametro_pesquisa_usuario:
                    filtro_encontrado = True
            case 4:
                if item.preco_pix == parametro_pesquisa_usuario:
                    filtro_encontrado = True
            case 5:
                if item.valor_parcela == parametro_pesquisa_usuario:
                    filtro_encontrado = True
            case 6:
                if item.numero_parcelas == parametro_pesquisa_usuario:
                    filtro_encontrado = True
            case 7:
                if item.informacoes_tecnicas.__contains__(parametro_pesquisa_usuario):
                    filtro_encontrado = True

        if filtro_encontrado:
             verificador = verifica_se_o_produto_existe(cursor, item.sku)
             print("Resultado encontrado: ")
             print("Informações técnicas: " + str(item.informacoes_tecnicas) + "\n"
                   + "Título do produto: " + item.titulo + "\n" + "Preço: " + item.preco + "\n"
                   + "SKU do produto: " + item.sku + "\n" + "Preço no PIX: " + item.preco_pix + "\n"
                   + "Número de parcelas: " + item.numero_parcelas + "\n" + "Valor da parcela: " + item.valor_parcela)
             if verificador:
                 atualizar_produto(conexao, cursor, item.titulo, item.preco, item.preco_pix, item.valor_parcela, item.numero_parcelas, item.informacoes_tecnicas, item.sku)
                 continue

             inserir_registro(conexao, cursor, item.titulo, item.preco, item.preco_pix, item.valor_parcela, item.numero_parcelas, item.informacoes_tecnicas, item.sku)
 except requests.exceptions.HTTPError as erro_http:
             print(f"Erro HTTP: {erro_http}")
             print(f"Status code: {erro_http.response.status_code}")
 except requests.exceptions.ConnectionError as erro_conexao:
            print(f"Erro de conexão: Não foi possível conectar ao servidor. {erro_conexao}")
 except requests.exceptions.Timeout as erro_timeout:
            print(f"Erro de timeout: A requisição demorou demais. {erro_timeout}")
 except requests.exceptions.RequestException as erro_geral:
            print(f"Erro na requisição: {erro_geral}")


def redireciona_links_varredura(parametro_pesquisa_usuario, opcao_digitada):

    lista_de_urls= ["https://www.lojamaeto.com/dia-dos-pais-ofertas-imperdiveis", "https://www.lojamaeto.com/banheiro",
                     "https://www.lojamaeto.com/construcao", "https://www.lojamaeto.com/iluminacao", "https://www.lojamaeto.com/lonas",
                     "https://www.lojamaeto.com/material-eletrico", "https://www.lojamaeto.com/lancamento-solara",
                     "https://www.lojamaeto.com/ventilacao", "https://www.lojamaeto.com/lavanderia", "https://www.lojamaeto.com/"]
    for item in lista_de_urls:
        pega_dados_da_url(item, parametro_pesquisa_usuario, opcao_digitada)

opcao_digitada = input(f"Digite agora o seu parâmetro de busca,"
      f" você pode pesquisar por: \n 1 ) SKU do produto \n 2 ) Título do produto"
      f" \n 3 ) Preço \n 4 ) Preço no PIX \n 5 ) Valor da Parcela \n 6 ) Número de parcelas \n 7 ) Informações técnicas \n Digite o número: \n")
parametro_pesquisa_usuario = input("Digite o que deseja encontrar: ")

if not opcao_digitada.isdigit() or not (1 <= int(opcao_digitada) <= 7):
    print("Opção inválida!")
    exit()

redireciona_links_varredura(parametro_pesquisa_usuario, opcao_digitada)






