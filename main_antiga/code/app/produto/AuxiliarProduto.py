from typing import List
from app.produto.Produto import Produto

class AuxiliarProduto:
    def ordena_valor(produtos: List[Produto], considerar_frete=True, decrescente=False)->List[Produto]:
        # garante que a lita não possua produtos com erro
        produtos_validos = [produto for produto in produtos if produto.valor >= 0]
        if considerar_frete:
            # ordena os valores considerando o valor_total = valor + frete
            ordenado_por_preco = sorted(
                produtos_validos, 
                key=lambda produto_valido: produto_valido.valor_total, 
                reverse=decrescente
                )
        else:
            # ordena os valores sem considerar o frete considernado só o valor
            ordenado_por_preco = sorted(
                produtos_validos, 
                key=lambda produto_valido: produto_valido.valor, 
                reverse=decrescente
                )
        return ordenado_por_preco