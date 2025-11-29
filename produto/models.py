from django.db import models
import re

# Create your models here.

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
    def filtrar_frete_gratis(produtos):
        # Filtra apenas produtos com frete grátis
        return [p for p in produtos if any(termo in p.frete.lower() 
                                         for termo in ['grátis', 'gratis', 'free', 'frete grátis', 'frete gratis', 'frete gratuito',
                                                        'GRÁTIS', 'GRATIS', 'FREE', 'FRETE GRÁTIS', 'FRETE GRATIS', 'FRETE GRATUITO'])]
    