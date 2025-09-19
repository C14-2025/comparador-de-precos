import pytest
from unittest.mock import Mock
from app.produto.AuxiliarProduto import AuxiliarProduto

@pytest.fixture
def lista_de_produtos_mock():
    # cria uma lista de produtos mokados para serem utilizados nos testes
    p1 = Mock()
    p1.nome = "Produto A"
    p1.valor = 50
    p1.valor_total = 125 # valor + frete

    p2 = Mock()
    p2.nome = "Produto B"
    p2.valor = 100
    p2.valor_total = 110 # valor + frete

    p3 = Mock()
    p3.nome = "Produto C"
    p3.valor = 200
    p3.valor_total = 275 # valor + frete

    p4_produto_invalido = Mock()
    p4_produto_invalido.nome = "Produto D INVALIDO"
    p4_produto_invalido.valor = -10
    p4_produto_invalido.valor_total = 20 # valor + frete

    return [p1, p2, p3, p4_produto_invalido]

def test_ordena_valor_remove_produtos_negativos(lista_de_produtos_mock):
    
    resultado = AuxiliarProduto.ordena_valor(lista_de_produtos_mock)
    
    assert len(resultado) == 3

    nomes_resultado = [produto.nome for produto in resultado]
    assert "Produto D INVALIDO" not in nomes_resultado

def test_ordena_valor_crescente_com_frete(lista_de_produtos_mock):
    resultado = AuxiliarProduto.ordena_valor(lista_de_produtos_mock)
    
    assert resultado[0].nome == "Produto B"
    assert resultado[1].nome == "Produto A"
    assert resultado[2].nome == "Produto C"

def test_ordena_valor_crecente_sem_frete(lista_de_produtos_mock):
    resultado = AuxiliarProduto.ordena_valor(lista_de_produtos_mock, considerar_frete=False)
    
    assert resultado[0].nome == "Produto A"
    assert resultado[1].nome == "Produto B"
    assert resultado[2].nome == "Produto C"

def test_ordena_valor_decrescente(lista_de_produtos_mock):
    resultado = AuxiliarProduto.ordena_valor(lista_de_produtos_mock, decrescente=True)
    
    assert resultado[0].nome == "Produto C"
    assert resultado[1].nome == "Produto A"
    assert resultado[2].nome == "Produto B"
