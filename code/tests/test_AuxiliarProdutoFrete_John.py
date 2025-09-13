#test_auxiliarProduto
import pytest as pt
import pandas as pd
import numpy as np

from app.busca.AuxiliarProduto import AuxiliarProduto



def test_produtos_TemEstoque():
    produto_testado = "Leite Integral Piracanjuba 1l" 
    produto_testado_estoque = 0
      
    assert produto_testado_estoque >= 1 
    
def test_produtos_frete_calculo():
    produto_testado = "Espada Magica da Hiper Morte Eterna Infinita"
    produto_testado_frete = -5
    
    assert produto_testado_frete >= 0
    
def test_produtos_cupom():
    produto_testado = "Dado de lados infinitos"
    produto_testado_preco = 9999
    produto_testado_frete = 10
    cupom = True
    
    if cupom == True : produto_testado_frete = 0
    
    assert produto_testado_frete == 0

    
    
    
