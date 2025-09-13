#test_auxiliarProduto
import pytest
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.AuxiliarProduto.AuxiliarProduto import calcula_frete

def test_frete_com_cupom_e_preco_baixo():
    assert calcula_frete(["Livro Bom", "Loja de Fodaongar", "BRL",50, 10, 60, "url=foda2", 4.4, 4, "nacional", 5, True]) == 10

def test_frete_sem_cupom():
    assert calcula_frete(["Espada Normal", "Loja de Fodaongar", "BRL",200, 20, 220, "url=foda3", 4.2, 4, "nacional", 5, False]) == 20

def test_frete_valor_exato_limite():
    assert calcula_frete(["Espada Ruim", "Loja de Fodaongar", "BRL",100, 20, 120, "url=foda4", 3.9, 4, "nacional", 5, True]) == 0