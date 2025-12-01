# produto/urls.py
from django.urls import path
from . import views
from .views import api_buscar_produtos

urlpatterns = [
    path("api/buscar/", api_buscar_produtos, name="api_buscar_produtos")
]