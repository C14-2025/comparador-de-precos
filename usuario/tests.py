from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario
from .serializers import UsuarioSerializer
from unittest.mock import patch


class AutenticacaoTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        self.usuario_data = {
            "nome": "Teste",
            "email": "teste@teste.com",
            "senha": "abc123$%6789",
            "cep": "76908249",
            "nacionalidade": "Brasileiro"
        }

    def test_cadastro_usuario_sucesso(self):
        response = self.client.post("/api/usuarios/cadastrar/", self.usuario_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        usuario = Usuario.objects.get(email="teste@teste.com")
        self.assertEqual(usuario.nome, "Teste")
        self.assertTrue(check_password("abc123$%6789", usuario.senha))

    def test_login_usuario_sucesso(self):
        self.client.post("/api/usuarios/cadastrar/", self.usuario_data, format="json")

        login_data = {"email": "teste@teste.com", "senha": "abc123$%6789"}
        response = self.client.post("/api/usuarios/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("usuario_id", response.data)
        self.assertIn("nome", response.data)

    def test_login_usuario_senha_errada(self):
        self.client.post("/api/usuarios/cadastrar/", self.usuario_data, format="json")
        login_data = {"email": "teste@teste.com", "senha": "senhaerrada"}
        response = self.client.post("/api/usuarios/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("erro", response.data)

    def test_login_usuario_email_invalido(self):
        login_data = {"email": "invalido@teste.com", "senha": "abc123$%6789"}
        response = self.client.post("/api/usuarios/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("erro", response.data)

class AutenticacaoMockTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("usuario.views.Usuario.objects.get")
    def test_login_usuario_mock_sucesso(self, mock_get):
        mock_usuario = mock_get.return_value
        mock_usuario.id = 1
        mock_usuario.nome = "Teste"
        mock_usuario.senha = "hash_fake"
        
        with patch("usuario.views.check_password", return_value=True):
            response = self.client.post("/api/usuarios/login/", {"email": "teste@teste.com", "senha": "senha123"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertIn("usuario_id", data)
            self.assertIn("nome", data)

    @patch("usuario.views.Usuario.objects.get")
    def test_login_usuario_mock_senha_errada(self, mock_get):
        mock_usuario = mock_get.return_value
        mock_usuario.senha = "hash_fake"
        
        with patch("usuario.views.check_password", return_value=False):
            response = self.client.post("/api/usuarios/login/", {"email": "teste@teste.com", "senha": "senharrrada"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            data = response.json()
            self.assertIn("erro", data)