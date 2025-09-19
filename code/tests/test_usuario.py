import pytest
from unittest.mock import patch, Mock
from app.usuario.Usuario import Usuario

@patch("requests.get")
def test_criar_conta_cep_inexistente(mock_get): # CEP que não existe
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "99999-999",
        20,
        "28-05-2003",
        "Brasileira"
    )
    
    mock_retorno = Mock()
    mock_retorno.json.return_value = {
        "erro": True
        }
    mock_get.return_value = mock_retorno

    with pytest.raises(ValueError, match="CEP inexistente"):
        novo_usuario.criar_conta()

@patch("requests.get")
def test_criar_conta_cep_nao_padrao(mock_get): # CEP válido porém com "-"
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "29196-015",
        20,
        "28-05-2003",
        "Brasileira"
    )

    mock_retorno = Mock()
    mock_retorno.json.return_value = {
        "cep": "29196-015",
        "logradouro": "Rua Eurico Conceição Cruz",
        "complemento": "",
        "unidade": "",
        "bairro": "Jacupemba",
        "localidade": "Aracruz",
        "uf": "ES",
        "estado": "Espírito Santo",
        "regiao": "Sudeste",
        "ibge": "3200607",
        "gia": "",
        "ddd": "27",
        "siafi": "5611"
        }
    mock_get.return_value = mock_retorno

    assert novo_usuario.criar_conta() is None

@patch("requests.get")
def test_criar_conta_cep_valido_padrao(mock_get): # CEP válido dentro do padrão (sem '-')
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "66630670",
        20,
        "28-05-2003",
        "Brasileira"
    )

    mock_retorno = Mock()
    mock_retorno.json.return_value = {
        "cep": "66630-670",
        "logradouro": "Rua José Machado",
        "complemento": "",
        "unidade": "",
        "bairro": "Bengui",
        "localidade": "Belém",
        "uf": "PA",
        "estado": "Pará",
        "regiao": "Norte",
        "ibge": "1501402",
        "gia": "",
        "ddd": "91",
        "siafi": "0427"
        }
    mock_get.return_value = mock_retorno

    assert novo_usuario.criar_conta() is None

def test_criar_conta_cep_invalido(): # CEP inválido (com mais de 8 digitos) -> nem chega a pegar a api
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "1234569999978",
        20,
        "28-05-2003",
        "Brasileira"
    )

    with pytest.raises(ValueError, match="CEP invalido"):
        novo_usuario.criar_conta()

@patch("requests.get")
def test_criar_conta_idade_invalida(mock_get): # idade inválida (numero negativo)
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "66630-670",
        -5,
        "28-05-2003",
        "Brasileira"
    )

    mock_retorno = Mock()
    mock_retorno.json.return_value = {
        "cep": "66630-670",
        "logradouro": "Rua José Machado",
        "complemento": "",
        "unidade": "",
        "bairro": "Bengui",
        "localidade": "Belém",
        "uf": "PA",
        "estado": "Pará",
        "regiao": "Norte",
        "ibge": "1501402",
        "gia": "",
        "ddd": "91",
        "siafi": "0427"
        }
    mock_get.return_value = mock_retorno

    with pytest.raises(ValueError, match="Idade invalida"):
        novo_usuario.criar_conta()

def test_criar_conta_faltando_dados(): # colocando dados a menos (não passa pela api)
    
    novo_usuario = Usuario(
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "66630-670",
        28,
        "28-05-2003",
        "Brasileira"
    )
    
    with pytest.raises(ValueError, match="Dados obrigatorios incompletos"):
        novo_usuario.criar_conta()
