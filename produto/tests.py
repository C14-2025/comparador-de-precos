from django.test import TestCase
from unittest.mock import MagicMock, patch

from produto.models import OrdenadorProdutos, FiltrosProdutos


# =============================================
#   TESTES UNITÁRIOS REAIS (SEM MOCK)
# =============================================

class TestUnitariosModels(TestCase):

    def test_extrair_numero_vendas_real(self):
        #valida regex
        self.assertEqual(OrdenadorProdutos.extrair_numero_vendas("50+"), 50)
        self.assertEqual(OrdenadorProdutos.extrair_numero_vendas("120 compras"), 120)
        self.assertEqual(OrdenadorProdutos.extrair_numero_vendas(""), 0)
        self.assertEqual(OrdenadorProdutos.extrair_numero_vendas("nao tem"), 0)

    def test_filtrar_por_loja_real(self):
        #filtro loja
        p1 = MagicMock(loja="Amazon")
        p2 = MagicMock(loja="Mercado Livre")
        p3 = MagicMock(loja="amazon")  # case-insensitive

        produtos = [p1, p2, p3]
        filtrados = FiltrosProdutos.filtrar_por_loja(produtos, "Amazon")

        self.assertEqual(filtrados, [p1, p3])
        

# =============================================
#   TESTES COM MOCK
# =============================================

class TestMocksModels(TestCase):

    @patch("produto.models.OrdenadorProdutos.ordenar_por_vendas")
    def test_mock_ordenar_por_vendas(self, mock_ordenar):
        mock_ordenar.return_value = ["fake", "lista"]

        from produto.models import OrdenadorProdutos

        res = OrdenadorProdutos.ordenar_por_vendas([])
        self.assertEqual(res, ["fake", "lista"])
        mock_ordenar.assert_called_once()


    @patch("produto.models.sorted")
    def test_mock_sorted_ordenar_preco(self, mock_sorted):
        #mock do sorted para verificar se é chamado corretamente
        productos_fake = ["X"]
        mock_sorted.return_value = ["ORDENADO"]

        resultado = OrdenadorProdutos.ordenar_por_preco(productos_fake)

        mock_sorted.assert_called_once()
        self.assertEqual(resultado, ["ORDENADO"])



    @patch("produto.models.re.findall")
    def test_mock_regex_extrair(self, mock_findall):
        #mock da regex para extrair número de vendas
        mock_findall.return_value = ["999"]

        result = OrdenadorProdutos.extrair_numero_vendas("qualquer coisa")

        self.assertEqual(result, 999)
        mock_findall.assert_called_once()



    @patch("produto.models.FiltrosProdutos.filtrar_por_faixa_preco")
    def test_mock_filter_preco(self, mock_filtrar):
        #mock do flitro por faixa de preço
        mock_filtrar.return_value = ["produto_filtrado"]

        result = FiltrosProdutos.filtrar_por_faixa_preco([], 10, 100)

        mock_filtrar.assert_called_once()
        self.assertEqual(result, ["produto_filtrado"])



    @patch("produto.models.FiltrosProdutos.filtrar_por_frete")
    def test_mock_filtro_frete(self, mock_frete):
        #mock do filtro frete gratis
        mock_frete.return_value = ["frete_gratis"]

        result = FiltrosProdutos.filtrar_por_frete(["x"])

        mock_frete.assert_called_once()
        self.assertEqual(result, ["frete_gratis"])
