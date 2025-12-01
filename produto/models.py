from django.db import models
import re

# Create your models here.

class Produto():
    def __init__(self, loja:str, link_produto: str, nome:str, moeda:str, preco:float, frete:str, frete_gratis:bool, nota:float, numero_vendas: str, imagem: str):
        self.loja = loja
        self.link_produto = link_produto
        self.nome = nome
        self.moeda = moeda
        self.preco = preco
        self.frete = frete
        self.frete_gratis = frete_gratis
        self.nota = nota
        self.numero_vendas = numero_vendas
        self.imagem = imagem


# Classes de ordenação que trabalham com os objetos Produto do MotorDeBusca
class OrdenadorProdutos:
    # Classe para ordenar produtos por diferentes critérios

    @staticmethod
    def extrair_numero_vendas(texto_vendas):
        # Extrai o número de vendas de strings como "50+", "100+ compras", etc.
        # Retorna 0 se não conseguir extrair

        if not texto_vendas or texto_vendas == "0":
            return 0
        
        try:
            # Remove caracteres não numéricos e extrai o primeiro número
            numeros = re.findall(r'\d+', texto_vendas)
            if numeros:
                return int(numeros[0])
            return 0
        except:
            return 0
    
    @staticmethod
    def ordenar_por_preco(produtos, ascendente=True):
        # Ordena por preço (menor para maior por padrão)
        return sorted(produtos, key=lambda x: x.preco, reverse=not ascendente)
    
    @staticmethod
    def ordenar_por_nota(produtos, ascendente=True):
        # Ordena por nota (maior nota primeiro por padrão)
        return sorted(produtos, key=lambda x: x.nota, reverse=not ascendente)
    
    @staticmethod
    def ordenar_por_vendas(produtos, ascendente=True):
        # Ordena por quantidade de vendas (mais vendidos primeiro por padrão)
        return sorted(produtos, key=lambda x: OrdenadorProdutos.extrair_numero_vendas(x.numero_vendas), reverse=not ascendente)

    @staticmethod
    def ordenar_por_loja(produtos):
        # Ordena por loja alfabeticamente
        return sorted(produtos, key=lambda x: x.loja)



class FiltrosProdutos:
    # Classes para filtrar produtos
    
    @staticmethod
    def filtrar_por_loja(produtos, loja):
        # Filtra produtos por loja específica
        return [p for p in produtos if p.loja.lower() == loja.lower()]
    
    @staticmethod
    def filtrar_por_faixa_preco(produtos, preco_min=0, preco_max=float('inf')):
        # Filtra produtos por faixa de preço
        return [p for p in produtos if preco_min <= float(p.preco) <= preco_max]
    
    @staticmethod
    def filtrar_por_nota_minima(produtos, nota_minima=0):
        # Filtra produtos com nota mínima
        return [p for p in produtos if float(p.nota) >= nota_minima]
    
    @staticmethod
    def filtrar_por_frete(produtos, frete_gratis=True):
        # Filtra produtos por condição de frete
        # frete_gratis=True: apenas produtos com frete grátis
        # frete_gratis=False: apenas produtos SEM frete grátis
        return [p for p in produtos if p.frete_gratis == frete_gratis]
    