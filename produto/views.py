from django.shortcuts import render

# Responsável por cuidar do que vai ser exibido
# Create your views here.

# def pesquisa(request): # Função para a página pesquisa da aplicação produto
#     return render(request, 'comparador_de_preco/produto/pesquisa.html')

# def resultado(request): # Função para a página resutado da aplicação produto
#     return render(request, 'comparador_de_preco/produto/resultado.html')



from django.http import HttpResponse # SÓ DE BRINCADEIRA PRA TESTAR

def teste(request):
    return HttpResponse('<h1>Bom dia para:</h1><p>Bia, Fefe, John, Chockito, China e o grande Vinnie!</p>')