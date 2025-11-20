# %%
import json
from bs4 import BeautifulSoup

class MotorDeBusca:
    def busca(produto: str)->str:
        pass

    def tratando_mercado_livre():
        with open('json_temp/pesquisa_mercado_livre_2.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

            produtos = []

            for dado in dados:
                produto = dado['html']
                soup = BeautifulSoup(produto, 'html.parser')

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

                preco_final_produto = f"{preco_inteiro_produto}.{preco_centavos_produto}"
                try:
                    preco_final_produto = float(preco_final_produto)
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

                produtos.append({
                    'loja': "Mercado Livre",
                    'nome': nome_produto,
                    'moeda': moeda_produto,
                    'preco_inteiro': preco_inteiro_produto,
                    'preco_centavos': preco_centavos_produto,
                    'preco': preco_final_produto,
                    'frete': frete_produto
                })

            return produtos
    
    def tratando_amazon():
        with open('json_temp/pesquisa_amazon_2.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

            produtos = []

            for dado in dados:
                produto = dado['html']
                
                soup = BeautifulSoup(produto, 'html.parser')
    
                # ======================== NOME ========================
                tag_nome = soup.find('h2')
                nome_produto = tag_nome.text.strip() if tag_nome else "Nome não encontrado"

                # ======================== PRECO =======================
                # TODO: CONVERTER MOEDA PARA O PADRAO (3 letras)
                tag_preco = soup.find('span', class_='a-offscreen')
                
                moeda_produto = "R$"
                preco_produto = "0,00"
                if tag_preco:
                    texto_preco = tag_preco.text.strip() 
                    try:
                        # Divide no espaço (R$ | 411,84)
                        partes = texto_preco.split(maxsplit=1) 
                        if len(partes) == 2:
                            moeda_produto = partes[0]
                            preco_produto = partes[1]
                        else:
                            preco_produto = texto_preco
                    except:
                        preco_produto = texto_preco

                # ======================== FRETE =======================
                tag_frete = soup.find('div', class_='udm-primary-delivery-message')
                
                if tag_frete:
                    frete_produto = " ".join(tag_frete.text.split())
                else:
                    frete_produto = "Frete não informado"

                produtos.append({
                    'loja': "Amazon",
                    'nome': nome_produto,
                    'moeda': moeda_produto,
                    'preco': preco_produto,
                    'frete': frete_produto
                })
            
            return produtos

    def tratando_():
        pass
# %%
produtos_dicionario_mercado_livre = MotorDeBusca.tratando_mercado_livre()
for produto in produtos_dicionario_mercado_livre:
    print(json.dumps(produto, indent=4, ensure_ascii=False))
# %%
produtos_dicionario_mercado_livre = MotorDeBusca.tratando_amazon()
for produto in produtos_dicionario_mercado_livre:
    print(json.dumps(produto, indent=4, ensure_ascii=False))

# %%
