from django.contrib import admin
from django.urls import include, path
from produto.views import teste # Apenas teste do django

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', teste) # Testando o django
    # path('produto/', include('produto.urls')), # FUNÇÃO PADRÃO PARA CAMINHO DOS URLS DE PRODUTO
    # path('usuario/', include('usuario.urls')), # FUNÇÃO PADRÃO PARA CAMINHO DOS URLS DE USUARIO
]
