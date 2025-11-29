import json
import os
import glob
import re

from crawling.amazon import AmazonCrawler
from crawling.mercado_livre import MercadoLivreCrawler
from bs4 import BeautifulSoup

# TODO: trocar a classe refactor_produto por produto
from refactor_produto import Produto


class MotorDeBusca:
    PATH_TEMP = 'app/json_temp'
    
    def busca(produto: str):
        AmazonCrawler().search(query=produto)
        MercadoLivreCrawler().search(query=produto)

        caminho_amazon = os.path.join(MotorDeBusca.PATH_TEMP, 'amazon.json')
        caminho_mlivre = os.path.join(MotorDeBusca.PATH_TEMP, 'mercado_livre.json')

        dados_amazon = MotorDeBusca.carregar_dados_json(caminho_amazon)
        dados_mlivre = MotorDeBusca.carregar_dados_json(caminho_mlivre)

        if dados_mlivre:
            produtos += MotorDeBusca.tratando_mercado_livre(dados_mlivre)
        
        if dados_amazon:
            produtos += MotorDeBusca.tratando_amazon(dados_amazon)

        MotorDeBusca.limpar_arquivos_temporarios()
        
        return produtos

    @staticmethod
    def removendo_arquivos(diretorio: str):
        os.remove(diretorio)

    @staticmethod
    def carregar_dados_json(caminho_arquivo: str) -> list:
        """Método auxiliar apenas para ler o arquivo."""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return []

    @staticmethod
    def tratando_mercado_livre(dados: list) -> list:
        produtos = []

        for dado in dados:
            soup = BeautifulSoup(dado.get('html', ''), 'html.parser')

            # ======================== NOME ========================
            tag_nome = soup.find('a', class_='poly-component__title')
            nome_produto = tag_nome.text.strip() if tag_nome else "Não encontrado"
            
            # ======================== PRECO =======================
            # TODO: CONVERTER MOEDA PARA O PADRAO (3 letras)
            tag_moeda = soup.find('span', class_='andes-money-amount__currency-symbol')
            moeda_produto = tag_moeda.text.strip() if tag_moeda else ""

            tag_inteiro = soup.find('span', class_='andes-money-amount__fraction')
            preco_inteiro_produto = tag_inteiro.text.strip() if tag_inteiro else "0"

            tag_centavos = soup.find('span', class_='andes-money-amount__cents')
            preco_centavos_produto = tag_centavos.text.strip() if tag_centavos else "00"

            # Remove pontos de milhar (ex: 1.200 -> 1200) para conversão correta
            # O Mercado Livre separa visualmente, mas precisamos de um float limpo
            preco_inteiro_limpo = preco_inteiro_produto.replace('.', '')
            
            string_valor = f"{preco_inteiro_limpo}.{preco_centavos_produto}"
            
            try:
                preco_final_produto = float(string_valor)
            except ValueError:
                preco_final_produto = 0.0

            # ======================== FRETE =======================
            tag_frete_rapido = soup.find('span', class_='poly-shipping--next_day')

            frete_produto = ''
            if tag_frete_rapido:
                frete_produto = tag_frete_rapido.text.strip()
            else:
                tag_frete_normal = soup.find('div', class_='poly-component__shipping')
                if tag_frete_normal:
                    frete_produto = tag_frete_normal.text.strip()
                else:
                    frete_produto = "Frete Indisponível"

            produto = Produto(
                loja="Mercado Livre",
                nome=nome_produto,
                moeda=moeda_produto,
                preco=preco_final_produto,
                frete=frete_produto                    
            )

            produtos.append(produto)

    @staticmethod
    def tratando_amazon(dados: list) -> list:
        produtos = []

        for dado in dados:
            soup = BeautifulSoup(dado.get('html', ''), 'html.parser')

            # ======================== NOME ========================
            tag_nome = soup.find('h2')
            nome_produto = tag_nome.text.strip() if tag_nome else "Nome não encontrado"

            # ======================== PRECO =======================
            tag_preco = soup.find('span', class_='a-offscreen')
            
            moeda_produto = "R$"
            valor_numerico = 0.0

            if tag_preco:
                texto_preco = tag_preco.text.strip()
                
                partes = texto_preco.split(maxsplit=1) 
                
                string_valor = ""

                if len(partes) == 2:
                    moeda_produto = str(partes[0])
                    string_valor = str(partes[1])
                else:
                    string_valor = re.sub(r'[^\d,.]', '', texto_preco)

                    if texto_preco.startswith("US$") or texto_preco.startswith("$"):
                        moeda_produto = "$"

                if ',' in string_valor and '.' in string_valor:
                        string_valor = string_valor.replace('.', '').replace(',', '.')

                elif ',' in string_valor:
                        string_valor = string_valor.replace(',', '.')
                
                try:
                    valor_numerico = float(string_valor)
                except ValueError:
                    valor_numerico = 0.0
            
            # ======================== FRETE =======================
            tag_frete = soup.find('div', class_='udm-primary-delivery-message')
            if tag_frete:
                frete_produto = " ".join(tag_frete.text.split())
            else:
                frete_produto = "Frete Indisponível. Consultar no Site"

            produto = Produto(
                loja="Amazon",
                nome=nome_produto,
                moeda=moeda_produto,
                preco=valor_numerico,
                frete=frete_produto
            )
            produtos.append(produto)
            
        return produtos
    