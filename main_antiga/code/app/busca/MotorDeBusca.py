import pandas as pd

class MonitorDeBusca:
    def catalogo_completo(arquivo: str) -> str:
        df = pd.read_csv(arquivo) # importando os dados
        produtos = ""

        for index, produto in df.iterrows(): # criando um log simples
            produtos += f"""
================= {produto['nome']} =================
Loja: {produto['loja']}
Moeda: {produto['moeda']}
Valor: R$ {produto['valor']:.2f}
Frete: R$ {produto['frete']:.2f}
Valor Total: R$ {produto['valor_total']:.2f}
Link: {produto['link']}
Nota: {produto['nota']}/5.0
Estoque: {produto['estoque']} unidades
Tipo de Envio: {produto['tipo_envio']}
Tempo de Entrega: {produto['tempo_entrega']}
Cupom Disponível: {'Sim' if produto['cupom'] else 'Não'}
"""
        return produtos

    def busca_produto(nome_produto: str, arquivo: str) -> list:
        df = pd.read_csv(arquivo) # importanto os dados
        produtos_buscados = df[df['nome'].str.contains(nome_produto.strip(), case=False)] # buscando produto com sequencia de caracteres iguais
        
        produtos = ""

        if produtos_buscados.empty: # retorno vazio
            return "Nenhum Produto Com Esse Nome Encontrado!!!" 

        for index, produto in produtos_buscados.iterrows(): # criando um log simples
            produtos = f"""
================= {produto['nome']} =================
Loja: {produto['loja']}
Moeda: {produto['moeda']}
Valor: R$ {produto['valor']:.2f}
Frete: R$ {produto['frete']:.2f}
Valor Total: R$ {produto['valor_total']:.2f}
Link: {produto['link']}
Nota: {produto['nota']}/5.0
Estoque: {produto['estoque']} unidades
Tipo de Envio: {produto['tipo_envio']}
Tempo de Entrega: {produto['tempo_entrega']}
Cupom Disponível: {'Sim' if produto['cupom'] else 'Não'}
\n\n
"""
        return produtos