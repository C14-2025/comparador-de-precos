import pytest

from app.usuario import Usuario

def test_criar_conta_cep_padrao(): # CEP completamente dentro do padrão XXXXX-XXX
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "12345-678",
        20,
        "28-05-2003",
        "Brasileira"
    )

    assert novo_usuario.criar_conta() is None

def test_criar_conta_cep_valido_nao_padrao(): # CEP válido (8 digitos numericos) mas fora do padrão (sem '-')
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "12345678",
        20,
        "28-05-2003",
        "Brasileira"
    )

    assert novo_usuario.criar_conta() is None

def test_criar_conta_cep_valido_invalido(): # CEP válido (8 digitos numericos) mas fora do padrão (sem '-')
    novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "1234569999978",
        20,
        "28-05-2003",
        "Brasileira"
    )

    assert novo_usuario.criar_conta() == "CEP invalido"

def test_idade_invalida():
        novo_usuario = Usuario(
        "Beatriz",
        "beatriz.cardozo@ges.inatel.br",
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "1234569999978",
        -5
        "28-05-2003",
        "Brasileira"
    )
    assert novo_usuario.criar_conta() == "Erro ao criar conta"

def test_faltando_dados():
    novo_usuario = Usuario(
        "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cac",
        "1234569999978",
        -5
        "28-05-2003",
        "Brasileira"
    )
    assert novo_usuario.criar_conta() == "Erro ao criar conta"