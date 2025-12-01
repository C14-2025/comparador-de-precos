from django.test import TestCase
from unittest.mock import MagicMock
import sys

class TestUnitariosModels(TestCase):
    #=================================================
    # Testes sem MOCKS - testam a implementação real
    #=================================================
    
    def setUp(self):
        
        #remove os modulos da memória para evitar vazamento entre testes.
        modules_to_delete = []
        for module_name in sys.modules:
            if module_name.startswith('produto.'):
                modules_to_delete.append(module_name)
        
        for module_name in modules_to_delete:
            del sys.modules[module_name]
    
    def test_extrair_numero_vendas_real(self):
        # import DEPOIS de limpar o cache
        from produto.models import OrdenadorProdutos
        
        
        metodo = OrdenadorProdutos.extrair_numero_vendas
        print(f"DEBUG - Tipo do método: {type(metodo)}")
        print(f"DEBUG - É callable? {callable(metodo)}")
        
        #test
        resultado = metodo("50+")
        print(f"DEBUG - Resultado para '50+': {resultado}")
        
        self.assertEqual(resultado, 50)
        self.assertEqual(OrdenadorProdutos.extrair_numero_vendas("120 compras"), 120)
        self.assertEqual(OrdenadorProdutos.extrair_numero_vendas(""), 0)
        self.assertEqual(OrdenadorProdutos.extrair_numero_vendas("nao tem"), 0)

    def test_filtrar_por_loja_real(self):
        #import depois de limpar o cahce
        from produto.models import FiltrosProdutos
        
        #cria mocks locais para produtos
        p1 = MagicMock(loja="Amazon")
        p2 = MagicMock(loja="Mercado Livre")
        p3 = MagicMock(loja="amazon")

        produtos = [p1, p2, p3]
        filtrados = FiltrosProdutos.filtrar_por_loja(produtos, "Amazon")

        self.assertEqual(filtrados, [p1, p3])