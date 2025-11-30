from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Usuario
from .serializers import UsuarioSerializer

@api_view(['POST'])
def cadastrar_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensagem": "Usuário criado com sucesso!"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_usuario(request):
    email = request.data.get("email")
    senha = request.data.get("senha")

    try:
        user = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response({"erro": "Email não encontrado"}, status=404)

    if check_password(senha, user.senha):
        return Response({"mensagem": "Login ok", "usuario_id": user.id})
    else:
        return Response({"erro": "Senha incorreta"}, status=400)
