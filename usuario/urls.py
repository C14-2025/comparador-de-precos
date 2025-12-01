from django.urls import path
from .views import cadastrar_usuario, login_usuario

urlpatterns = [
    path('cadastrar/', cadastrar_usuario),
    path('login/', login_usuario),
]
