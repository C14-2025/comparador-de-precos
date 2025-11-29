from django.shortcuts import render
from django.http import HttpResponse
import sys
import os

from django.shortcuts import render
from django.http import HttpResponse
import sys
import os

def pagina_inicial(request):
    """Página inicial com formulário de pesquisa"""
    return render(request, 'produto/pesquisa.html')

def buscar_produtos(request):
    """Processa a busca e mostra resultados"""
    produto = request.GET.get('produto', '')
    criterio = request.GET.get('ordenar', 'preco')  # Parâmetro para ordenação
    
    if not produto:
        return render(request, 'produto/pesquisa.html', {'erro': 'Digite um produto para buscar'})
    
    try:
        # Configura o caminho para importação
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        busca_crawler_path = os.path.join(project_root, 'buscaCrawler')
        
        if busca_crawler_path not in sys.path:
            sys.path.append(busca_crawler_path)
        
        from buscaCrawler.motor_busca import MotorDeBusca
        from .models import OrdenadorProdutos
        
        # Busca produtos
        produtos = MotorDeBusca.busca(produto)
        
        # Aplica ordenação baseada no critério selecionado
        if criterio == 'preco':
            produtos_ordenados = OrdenadorProdutos.ordenar_por_preco(produtos, ascendente=True)
        elif criterio == 'preco_desc':
            produtos_ordenados = OrdenadorProdutos.ordenar_por_preco(produtos, ascendente=False)
        elif criterio == 'nota':
            produtos_ordenados = OrdenadorProdutos.ordenar_por_nota(produtos)
        elif criterio == 'vendas':
            produtos_ordenados = OrdenadorProdutos.ordenar_por_vendas(produtos)
        elif criterio == 'loja':
            produtos_ordenados = OrdenadorProdutos.ordenar_por_loja(produtos)
        else:
            produtos_ordenados = produtos  # Sem ordenação
        
        context = {
            'produto_busca': produto,
            'produtos': produtos_ordenados,
            'total_produtos': len(produtos_ordenados),
            'criterio_selecionado': criterio
        }
        
        return render(request, 'produto/resultado.html', context)
        
    except Exception as e:
        error_msg = f"Erro na busca: {str(e)}"
        return render(request, 'produto/pesquisa.html', {'erro': error_msg})