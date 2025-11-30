# produto/views.py
from django.shortcuts import render
import sys
import os

def pagina_inicial(request):
    """
    View para a página inicial do comparador de preços.
    
    Esta função é responsável por renderizar a página principal 
    onde o usuário pode digitar o produto que deseja buscar.
    
    Args:
        request: Objeto HttpRequest contendo os dados da requisição
        
    Returns:
        HttpResponse: Renderiza o template de pesquisa
    """
    # Renderiza o template 'produto/pesquisa.html' que contém o formulário de busca
    return render(request, 'produto/pesquisa.html')

def buscar_produtos(request):
    """
    View para processar a busca de produtos e exibir os resultados.
    
    Esta função:
    1. Recebe os parâmetros da busca via GET
    2. Valida se o produto foi informado
    3. Importa e utiliza o MotorDeBusca para buscar produtos
    4. Aplica ordenação conforme critério selecionado
    5. Renderiza os resultados ou exibe erro
    
    Args:
        request: Objeto HttpRequest com os parâmetros GET
        
    Returns:
        HttpResponse: Template com resultados ou mensagem de erro
    """
    # Obtém o termo de busca dos parâmetros GET, padrão é string vazia
    produto = request.GET.get('produto', '')
    # Obtém o critério de ordenação, padrão é 'preco' (menor preço primeiro)
    criterio = request.GET.get('ordenar', 'preco')
    
    # Validação: verifica se o usuário digitou algo para buscar
    if not produto:
        # Se não digitou, retorna à página de pesquisa com mensagem de erro
        return render(request, 'produto/pesquisa.html', {'erro': 'Digite um produto para buscar'})
    
    try:
        # CONFIGURAÇÃO DE IMPORTAÇÃO
        # Obtém o caminho absoluto do diretório raiz do projeto
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Constrói o caminho completo para a pasta buscaCrawler
        busca_crawler_path = os.path.join(project_root, 'buscaCrawler')
        
        # Adiciona o caminho ao sys.path para permitir importação do módulo
        if busca_crawler_path not in sys.path:
            sys.path.append(busca_crawler_path)
        
        # IMPORTAÇÃO DOS MÓDULOS NECESSÁRIOS
        # Importa a classe MotorDeBusca que faz o web scraping
        from buscaCrawler.motor_busca import MotorDeBusca
        # Importa a classe OrdenadorProdutos que contém os métodos de ordenação
        from .models import OrdenadorProdutos
        
        # EXECUÇÃO DA BUSCA
        # Chama o método busca do MotorDeBusca para obter a lista de produtos
        # Este método faz web scraping na Amazon e Mercado Livre
        produtos = MotorDeBusca.busca(produto)
        
        # APLICAÇÃO DA ORDENAÇÃO
        # Seleciona o método de ordenação baseado no critério escolhido pelo usuário
        if criterio == 'preco':
            # Ordena por preço em ordem crescente (menor preço primeiro)
            produtos_ordenados = OrdenadorProdutos.ordenar_por_preco(produtos, ascendente=True)
        elif criterio == 'preco_desc':
            # Ordena por preço em ordem decrescente (maior preço primeiro)
            produtos_ordenados = OrdenadorProdutos.ordenar_por_preco(produtos, ascendente=False)
        elif criterio == 'nota':
            # Ordena por nota de avaliação (maior nota primeiro)
            produtos_ordenados = OrdenadorProdutos.ordenar_por_nota(produtos)
        elif criterio == 'vendas':
            # Ordena por quantidade de vendas (mais vendidos primeiro)
            produtos_ordenados = OrdenadorProdutos.ordenar_por_vendas(produtos)
        elif criterio == 'loja':
            # Ordena por nome da loja (ordem alfabética)
            produtos_ordenados = OrdenadorProdutos.ordenar_por_loja(produtos)
        else:
            # Se critério não reconhecido, usa lista sem ordenação
            produtos_ordenados = produtos
        
        # PREPARAÇÃO DOS DADOS PARA O TEMPLATE
        # Cria o dicionário de contexto com os dados que serão passados para o template
        context = {
            'produto_busca': produto,           # Termo que o usuário buscou
            'produtos': produtos_ordenados,     # Lista de produtos ordenada
            'total_produtos': len(produtos_ordenados),  # Quantidade total de produtos
            'criterio_selecionado': criterio    # Critério de ordenação usado
        }
        
        # RENDERIZAÇÃO DOS RESULTADOS
        # Renderiza o template de resultados com os dados processados
        return render(request, 'produto/resultado.html', context)
        
    except Exception as e:
        # TRATAMENTO DE ERROS
        # Captura qualquer exceção que ocorra durante o processo
        error_msg = f"Erro na busca: {str(e)}"
        # Retorna à página de pesquisa exibindo a mensagem de erro
        return render(request, 'produto/pesquisa.html', {'erro': error_msg})