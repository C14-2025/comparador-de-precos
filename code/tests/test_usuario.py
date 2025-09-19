import pytest

from app.usuario.Usuario import Usuario

def test_criar_conta_cep_nao_padrao(): # CEP válido porém com "-"
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "29196-015",
        20,
        "28-05-2003",
        "Brasileira"
    )

    assert novo_usuario.criar_conta() is None

def test_criar_conta_cep_valido_padrao(): # CEP válido dentro do padrão (sem '-')
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "66630670",
        20,
        "28-05-2003",
        "Brasileira"
    )

    assert novo_usuario.criar_conta() is None

def test_criar_conta_cep_invalido(): # CEP inválido (com mais de 8 digitos)
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

def test_criar_conta__idade_invalida():
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "28909-040",
        -5,
        "28-05-2003",
        "Brasileira"
    )
    with pytest.raises(ValueError, match="Idade invalida"):
        novo_usuario.criar_conta()

def test_criar_conta__faltando_dados():
    
    novo_usuario = Usuario(
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "28909-040",
        28,
        "28-05-2003",
        "Brasileira"
    )
    with pytest.raises(ValueError, match="Dados obrigatorios incompletos"):
        novo_usuario.criar_conta()