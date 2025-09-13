# test_cadastro.py
import unittest
from Cadastro import Cadastro
from Usuario import Usuario

class TestCadastro(unittest.TestCase):
    def setUp(self):
        self.cad = Cadastro()

    # ---------- positivos (senhas fortes) ----------
    def test_cadastrar_com_senha_forte_retorna_usuario(self):
        u = self.cad.cadastrar("Joao", "joao@example.com", "Aa1!aaaaaaaa")
        self.assertIsNotNone(u, "Deve retornar um Usuario quando a senha é forte")
        self.assertIsInstance(u, Usuario)
        self.assertEqual(u.nome, "Joao")
        self.assertEqual(u.email, "joao@example.com")

    def test_cadastrar_senhas_com_caracteres_especiais_complexos(self):
        u = self.cad.cadastrar("Pedro", "pedro@ex.com", "XyZ9~@;:.,!abcd")
        self.assertIsNotNone(u)
        self.assertIsInstance(u, Usuario)

    # ---------- negativos (senhas fracas) ----------
    def test_senha_muito_curta_rejeitada(self):
        u = self.cad.cadastrar("Ana", "ana@example.com", "Aa1!aaa")  # menor que 12
        self.assertIsNone(u, "Senha curta deve resultar em None (rejeitada)")

    def test_senha_sem_caracter_especial_rejeitada(self):
        u = self.cad.cadastrar("Luiz", "luiz@example.com", "Aa1aaaaaaaaa")  # sem special
        self.assertIsNone(u)

if __name__ == "__main__":
    unittest.main()
