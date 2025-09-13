import pytest

from app.produto.Produto import Produto


def test_converter_preco_corretamente():
    p = Produto("Beyblade", "USD", 100, 20, "letitrip.com", 4.5, 10, "Internacional - USA", False)
    valor_convertido = p.converter_preco(5,p.valor) # USD = 5 BRL valor = 100  conversao = 100*5
    assert valor_convertido == 500

def test_somar_valor_com_frete():
    p = Produto("Beyblade", "USD", 100, 20, "letitrip.com", 4.5, 10, "Internacional - USA", False)
    p.somar_valor() # valor = 100 | frete = 20 | 100 + 20 = 120
    assert p.valor_total == 120

#poderia até criar um desse pra cada variavel mas seria o mesmo teste, não acho que estaria aumentando a qualidade do código
def test_criar_produto_com_valor_negativo():
    with pytest.raises(ValueError, match="O valor do produto não pode ser negativo"):
        p = Produto("Beyblade", "USD", -10, 20, "letitrip.com", 4.5, 10, "Internacional - USA", False)

