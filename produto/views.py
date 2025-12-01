from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import sys, os
from .serializers import ProdutoSerializer

@api_view(["GET"])
def api_buscar_produtos(request):
    produto = request.GET.get("produto", "")
    criterio = request.GET.get("ordenar", "preco")

    if produto == "":
        return Response({"erro": "Produto não informado"}, status=400)

    try:
        # Importação dinâmica do motor de busca
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        crawler_path = os.path.join(project_root, "buscaCrawler")

        if crawler_path not in sys.path:
            sys.path.append(crawler_path)

        from buscaCrawler.motor_busca import MotorDeBusca
        from .models import OrdenadorProdutos

        produtos = MotorDeBusca.busca(produto)

        # Ordenação
        if criterio == "preco":
            produtos = OrdenadorProdutos.ordenar_por_preco(produtos)
        elif criterio == "preco_desc":
            produtos = OrdenadorProdutos.ordenar_por_preco(produtos, ascendente=False)
        elif criterio == "nota":
            produtos = OrdenadorProdutos.ordenar_por_nota(produtos)
        elif criterio == "vendas":
            produtos = OrdenadorProdutos.ordenar_por_vendas(produtos)
        elif criterio == "loja":
            produtos = OrdenadorProdutos.ordenar_por_loja(produtos)

        serializer = ProdutoSerializer(produtos, many=True)

        return Response(serializer.data)

    except Exception as e:
        return Response({"erro": str(e)}, status=500)
