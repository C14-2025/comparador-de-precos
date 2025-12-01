from django.test import TestCase
from unittest.mock import patch, MagicMock
import sys

class TestMocksModels(TestCase):
    #=================================================
    # TESTES DE MOCKS TESTANDO A IMPLEMENTAÇÃO MOCKADA
    #=================================================
    
    def setUp(self):
        #limpa o cache dos módulos antes de cada teste, para evitar erro de vazamento.
        modules_to_delete = []
        for module_name in sys.modules:
            if module_name.startswith('produto.'):
                modules_to_delete.append(module_name)
        
        for module_name in modules_to_delete:
            del sys.modules[module_name]
    
    def test_mock_ordenar_por_vendas(self):
        # mock do método ordenar_por_vendas
        # Patch usando caminho absoluto
        with patch('produto.models.OrdenadorProdutos.ordenar_por_vendas') as mock_ordenar:
            mock_ordenar.return_value = ["fake", "lista"]
            
            from produto.models import OrdenadorProdutos
            res = OrdenadorProdutos.ordenar_por_vendas([])
            
            self.assertEqual(res, ["fake", "lista"])
            mock_ordenar.assert_called_once()

    def test_mock_sorted_ordenar_preco(self):
        
        # mock da função built-in sorted usada no método ordenra_por_preco 
        with patch('builtins.sorted') as mock_sorted:
            mock_sorted.return_value = ["ORDENADO"]
            
            from produto.models import OrdenadorProdutos
            resultado = OrdenadorProdutos.ordenar_por_preco(["X"])
            
            mock_sorted.assert_called_once()
            self.assertEqual(resultado, ["ORDENADO"])

    def test_mock_regex_extrair(self):
        # mock regex usado no método extrair_numero_vendas
        with patch('produto.models.re.findall') as mock_findall:
            mock_findall.return_value = ["999"]
            
            from produto.models import OrdenadorProdutos
            result = OrdenadorProdutos.extrair_numero_vendas("qualquer coisa")
            
            self.assertEqual(result, 999)
            mock_findall.assert_called_once()

    def test_mock_filter_preco(self):
        
        with patch('produto.models.FiltrosProdutos.filtrar_por_faixa_preco') as mock_filtrar:
            mock_filtrar.return_value = ["produto_filtrado"]
            
            from produto.models import FiltrosProdutos
            result = FiltrosProdutos.filtrar_por_faixa_preco([], 10, 100)
            
            mock_filtrar.assert_called_once()
            self.assertEqual(result, ["produto_filtrado"])

    def test_mock_filtro_frete(self):
        
        with patch('produto.models.FiltrosProdutos.filtrar_por_frete') as mock_frete:
            mock_frete.return_value = ["frete_gratis"]
            
            from produto.models import FiltrosProdutos
            result = FiltrosProdutos.filtrar_por_frete(["x"])
            
            mock_frete.assert_called_once()
            self.assertEqual(result, ["frete_gratis"])