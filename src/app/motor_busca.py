# %%
import json
from bs4 import BeautifulSoup
import re   

class MotorDeBusca:
    def busca(produto: str)->str:
        pass

    def tratando_mercado_livre():
        with open('json_temp/pesquisa_mercado_livre.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

            produtos = []

            for dado in dados:
                produto = dado['html']

                # ======================== NOME ========================
                match_nome = re.search(r'class="poly-component__title"[^>]*>(.*?)</a>', produto)
                nome_produto = match_nome.group(1) if match_nome else "Não encontrado"
                
                # ======================== PRECO =======================
                # TODO: CONVERTER MOEDA PARA O PADRAO (3 letras)
                match_moeda = re.search(r'class="andes-money-amount__currency-symbol">(.+?)</span>', produto)
                moeda_produto = match_moeda.group(1) if match_moeda else ""

                match_inteiro = re.search(r'class="andes-money-amount__fraction">(\d+)</span>', produto)
                preco_inteiro_produto = match_inteiro.group(1) if match_inteiro else "0"

                match_centavos = re.search(r'class="andes-money-amount__cents[^>]*">(\d+)</span>', produto)
                preco_centavos_produto = match_centavos.group(1) if match_centavos else "00"

                preco_final_produto = f"{preco_inteiro_produto}.{preco_centavos_produto}"
                preco_final_produto = float(preco_final_produto)

                # ======================== FRETE =======================
                match_frete_rapido = re.search(r'class="poly-shipping--next_day">(.+?)</span>', produto)

                frete_produto = ''
                if match_frete_rapido:
                    frete_produto = match_frete_rapido.group(1) # Vai pegar só "Chegará grátis amanhã"
                else:
                    
                    match_frete_normal = re.search(r'class="poly-component__shipping">(.+?)</div>', produto)
                    if match_frete_normal:
                        frete_produto = match_frete_normal.group(1)
                    else:
                        frete_produto = "Frete Indisponível"

                produtos.append({
                    'nome': nome_produto,
                    'moeda': moeda_produto,
                    'preco_inteiro': preco_inteiro_produto,
                    'preco_centavos': preco_centavos_produto,
                    'preco': preco_final_produto,
                    'frete': frete_produto
                })

            return produtos
    
    def tratando_amazon():
        pass

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
