# produto/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('buscar/', views.buscar_produtos, name='buscar_produtos'),
]