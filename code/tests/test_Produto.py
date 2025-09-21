import pytest
from unittest.mock import patch, Mock

from app.produto.Produto import Produto

#def test_somar_valor_com_frete():
#    p = Produto("Beyblade", "USD", 100, 20, "letitrip.com", 4.5, 10, "Internacional - USA", False)
#    p.somar_valor_frete() # valor = 100 | frete = 20 | 100 + 20 = 120
#    assert p.valor_total == 120

# def test_converter_preco_corretamente():
#    p = Produto("Beyblade", "USD", 100, 20, "letitrip.com", 4.5, 10, "Internacional - USA", False)
#    valor_convertido = p.converter_preco(5,p.valor) # USD = 5 BRL valor = 100  conversao = 100*5
#    assert valor_convertido == 500

# Teste básicaço só checando a criação de um produto
def test_cria_produto():
    p = Produto("Beyblade", "USD", 10, 20, "letitrip.com", 4.5, 10, "Internacional - USA", False)
    assert p.valor == 10


#poderia até criar um desse pra cada variavel mas seria o mesmo teste, não acho que estaria aumentando a qualidade do código
def test_criar_produto_com_valor_negativo():
    with pytest.raises(ValueError, match="O valor do produto não pode ser negativo"):
        p = Produto("Beyblade", "USD", -10, 20, "letitrip.com", 4.5, 10, "Internacional - USA", False)

# Removi o teste anterior de conversão de preço porque eu mudei a lógica para aceitar a api, deixei comentado ali em cima só por via das duvidas, mas não vai funcionar depois
# da adição da api :/ só deixando avisado caso veja a entrega anterior dos testes unitarios sem mock depois da entrega do mock
@patch('requests.get')
def test_converter_preco_correto(mock_get):
    mock_resposta = Mock()
    # vou criar como se fosse um produto em dolar!
    p = Produto("Action Figure do Gragas", "USD", 500, 100, "goidefanclub.us", 4.8, 3, "Internacional - USA", False)
    dict_resposta = {'date': '2025-09-20', 'usd': {"brl": 5.32085056, "jpy": 147.96595498, "eur": 0.85159403,} }
    mock_resposta.json.return_value = dict_resposta
    mock_get.return_value = mock_resposta
    assert p.converter_preco() == 2660.42528    

# Tive que alterar o teste do calculo do valor + frete também, deixei ambos comentados só por via das duvidas
@patch('requests.get')
def test_somar_frete_correto(mock_get):
    mock_resposta = Mock()
    dict_resposta = {'date': '2025-09-20', 'eur': {'jpy': 173.75175185, 'brl': 6.24810692, 'usd': 1.17426844, 'btc': 0.000010140043}}
    mock_resposta.json.return_value = dict_resposta
    mock_get.return_value = mock_resposta
    # vou criar esse como se fosse em euro
    p = Produto("Disco de Vinil Turn Blue do The Black Keys", "EUR", 60, 60, "theblackkeys.eu", 5, 500, "Internacional - Europe", False)

    assert p.valor_total == (60 * 6.24810692) + 60  # A soma do frete é feita diretamente no construtor, então não precisa chamar a função em si


def testar_somar_frete_em_real():
    # como não tem moeda estrangeira não precisa da api pra conversão, isso não tinha sido testado ainda
    p = Produto("Poster 2pac all eyez on me", "brl", 30, 22, "mercadolivre.inatel", 4.7, 20, "Nacional", False)
    assert p.valor_total == 52