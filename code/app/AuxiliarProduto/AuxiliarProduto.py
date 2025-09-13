from datetime import datetime
from typing import List

class Produto:
    def __init__(self, nome: str, loja: str, moeda: str, valor: float, frete: float, 
                 valor_total: float, link: str, nota: float, estoque: int, 
                 tipo_envio: str, tempo_entrega: datetime, cupom: bool):
        self.nome = nome
        self.loja = loja
        self.moeda = moeda
        self.valor = valor
        self.frete = frete
        self.valor_total = valor_total
        self.link = link
        self.nota = nota
        self.estoque = estoque
        self.tipo_envio = tipo_envio
        self.tempo_entrega = tempo_entrega
        self.cupom = cupom

    def __repr__(self):
        return f"Produto(nome = '{self.nome}', valor_total = {self.valor_total})"


#*Ordena preços do mais barato para o mais caro
def ordena_preco(produtos: List[Produto]) -> List[Produto]:
    return sorted(produtos, key = lambda x: x.valor_total)
        

#*Calcula o frete do produto
def calcula_frete(produtos: List[Produto]) -> List[Produto]:

    for produto in produtos:

        if "internacional" in produto.tipo_envio.lower():
            #Simula um cálculo de frete baseado no valor do produto
            produto.frete = produto.valor * 0.92 #considera o imposto

        elif "nacional" in produto.tipo_envio.lower():
            #Simula um cálculo de frete baseado no valor do produto
            produto.frete = produto.valor * 0.1 #Simula o frete como 10% do valor do produto 
            produto.valor_total = produto.valor + produto.frete

        elif produto.cupom and produto.valor >= 100:
            produto.frete == 0

    return produtos


#*Ordena por tempo de entrega do mais rápido para o mais lento
def ordena_tempo(produtos: List[Produto]) -> List[Produto]:

    return sorted(produtos, key = lambda x: x.tempo_entrega)


#*Ordena por melhor nota
def ordena_nota(produtos: List[Produto]) -> List[Produto]:

    for produto in produtos:

        if produto.nota > 5.0:
            produto.nota = 5.0

        elif produto.nota < 0:
            produto.nota = 0

    return sorted(produtos, key = lambda x: x.nota, reverse = True)