# test_cadastro.py (pytest)
import pytest
from Cadastro import Cadastro
from Usuario import Usuario

@pytest.fixture
def cad():
    return Cadastro()

# ---------- positivos (senhas fortes) ----------
def test_cadastrar_com_senha_forte_retorna_usuario(cad):
    u = cad.cadastrar("Joao", "joao@example.com", "Aa1!aaaaaaaa")
    assert u is not None, "Deve retornar um Usuario quando a senha é forte"
    assert isinstance(u, Usuario)
    assert u.nome == "Joao"
    assert u.email == "joao@example.com"

def test_cadastrar_senhas_com_caracteres_especiais_complexos(cad):
    u = cad.cadastrar("Pedro", "pedro@ex.com", "XyZ9~@;:.,!abcd")
    assert u is not None
    assert isinstance(u, Usuario)

# ---------- negativos (senhas fracas) ----------
def test_senha_muito_curta_rejeitada(cad):
    u = cad.cadastrar("Ana", "ana@example.com", "Aa1!aaa")  # menor que 12
    assert u is None, "Senha curta deve resultar em None (rejeitada)"

def test_senha_sem_caracter_especial_rejeitada(cad):
    u = cad.cadastrar("Luiz", "luiz@example.com", "Aa1aaaaaaaaa")  # sem special
    assert u is None
