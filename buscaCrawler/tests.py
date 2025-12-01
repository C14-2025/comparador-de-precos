from django.test import TestCase
import sys
from unittest.mock import MagicMock, patch, call

from buscaCrawler.motor_busca import MotorDeBusca
from produto.models import Produto

sys.modules['produto.models'] = MagicMock()
sys.modules['produto.models'].Produto = Produto 


# DUMMY DA CLASSE PARA O TESTE RODAR
class Produto:
    def __init__(self, loja, nome, link_produto, moeda, preco, frete, frete_gratis, nota, numero_vendas, imagem):
        self.loja = loja
        self.nome = nome
        self.link_produto = link_produto
        self.moeda = moeda
        self.preco = preco
        self.frete = frete
        self.frete_gratis = frete_gratis
        self.nota = nota
        self.numero_vendas = numero_vendas
        self.imagem = imagem

sys.modules['produto.models'] = MagicMock()
sys.modules['produto.models'].Produto = Produto 

class TestMotorDeBusca(TestCase):

    # ======================== 1. TESTES DO MÉTODO AUXILIAR (tem_gratis) ========================    

    def test_tem_gratis_com_acentos(self):
        """Verifica se a normalização de texto funciona para acentos"""
        assert MotorDeBusca.tem_gratis("Frete Grátis") is True
        assert MotorDeBusca.tem_gratis("Envio GRÁTIS") is True
        assert MotorDeBusca.tem_gratis("gratis") is True
    
    def test_tem_gratis_negativo(self):
        """Verifica se retorna False quando não é grátis"""
        assert MotorDeBusca.tem_gratis("Frete R$ 20,00") is False
        assert MotorDeBusca.tem_gratis("Consultar frete") is False

    # ======================== 2. TESTES PARSER MERCADO LIVRE ===================================

    def test_ml_completo_com_frete_gratis(self):
        """Testa um HTML completo do ML com frete grátis, imagem e link"""
        html_input = """
        <html>
            <a class="poly-component__title" href="https://produto.mercadolivre.com.br/MLB-123">iPhone 15</a>
            
            <!-- Preço: 5.000,99 -->
            <span class="andes-money-amount__currency-symbol">R$</span>
            <span class="andes-money-amount__fraction">5.000</span>
            <span class="andes-money-amount__cents">99</span>
            
            <!-- Frete Grátis -->
            <span class="poly-shipping--next_day">Chegará grátis amanhã</span>
            
            <!-- Avaliação e Vendas -->
            <span class="poly-component__review-compacted">
                <span class="poly-phrase-label">4.8</span>
                <span class="poly-phrase-label">| +1000 vendidos</span>
            </span>
            
            <!-- Imagem -->
            <img class="poly-component__picture" src="https://img.ml.com/foto.jpg" />
        </html>
        """
        dados = [{"html": html_input}]
        
        resultado = MotorDeBusca.tratando_mercado_livre(dados)
        produto = resultado[0]

        assert produto.loja == "Mercado Livre"
        assert produto.nome == "iPhone 15"
        assert produto.link_produto == "https://produto.mercadolivre.com.br/MLB-123"
        assert produto.preco == 5000.99
        assert "grátis" in produto.frete.lower()
        assert produto.frete_gratis is True
        assert produto.nota == 4.8
        assert "+1000 vendidos" in produto.numero_vendas
        assert produto.imagem == "https://img.ml.com/foto.jpg"

    def test_ml_sem_link_e_imagem_lazy(self):
        """Testa fallback de link e imagem com lazy loading"""
        html_input = """
        <html>
            <!-- Título sem href -->
            <a class="poly-component__title">Produto Teste</a>
            
            <!-- Imagem Lazy Load -->
            <img class="poly-component__picture" data-src="https://img.ml.com/lazy.jpg" />
        </html>
        """
        dados = [{"html": html_input}]
        
        resultado = MotorDeBusca.tratando_mercado_livre(dados)
        produto = resultado[0]

        assert produto.link_produto == "Link não encontrado"
        assert produto.imagem == "https://img.ml.com/lazy.jpg"

    def test_ml_vendas_formatacao_suja(self):
        """Testa se a limpeza do '|' no texto de vendas funciona"""
        html_input = """
        <html>
            <a class="poly-component__title">Produto Teste</a>
            <span class="poly-component__review-compacted">
                <span class="poly-phrase-label">5.0</span>
                <!-- Texto com pipe e espaços extras -->
                <span class="poly-phrase-label"> |  500 vendidos  </span>
            </span>
        </html>
        """
        dados = [{"html": html_input}]
        resultado = MotorDeBusca.tratando_mercado_livre(dados)
        
        assert resultado[0].numero_vendas == "500 vendidos"

    def test_ml_preco_sem_centavos(self):
        """Testa produto sem a tag de centavos (deve assumir 00)"""
        html_input = """
        <html>
            <a class="poly-component__title">Produto Barato</a>
            <span class="andes-money-amount__fraction">100</span>
            <!-- Tag de centavos ausente -->
        </html>
        """
        dados = [{"html": html_input}]
        resultado = MotorDeBusca.tratando_mercado_livre(dados)
        
        assert resultado[0].preco == 100.00

    # ======================== 3. TESTES PARSER AMAZON ==========================================

    def test_amazon_completo_link_relativo(self):
        """Testa HTML Amazon verificando a concatenação do link relativo"""
        html_input = """
        <html>
            <h2>
                <a href="/dp/B08X">Kindle Paperwhite</a>
            </h2>
            
            <!-- Preço: R$ 800,00 -->
            <span class="a-price">
                <span class="a-offscreen">R$ 800,00</span>
            </span>
            
            <!-- Frete Pago -->
            <div class="udm-primary-delivery-message">R$ 20,00 de entrega</div>
            
            <!-- Vendas mês passado -->
            <span class="a-size-base a-color-secondary">200+ compras no mês passado</span>
            
            <img class="s-image" src="https://m.media-amazon.com/img.jpg" />
        </html>
        """
        dados = [{"html": html_input}]
        
        resultado = MotorDeBusca.tratando_amazon(dados)
        produto = resultado[0]

        assert produto.loja == "Amazon"
        assert produto.link_produto == "https://www.amazon.com.br/dp/B08X"
        assert produto.preco == 800.00
        assert produto.frete_gratis is False
        assert "200+" in produto.numero_vendas
        assert produto.imagem == "https://m.media-amazon.com/img.jpg"

    def test_amazon_preco_quebrado_logica_visual(self):
        """Testa o fallback de preço (Tentativa 2) quando não acha o a-offscreen"""
        html_input = """
        <html>
            <h2><a href="link">Teste Preço</a></h2>
            <span class="a-price">
                <!-- Sem a-offscreen, pegando pelos spans visuais -->
                <span class="a-price-whole">1.250</span>
                <span class="a-price-fraction">50</span>
            </span>
        </html>
        """
        dados = [{"html": html_input}]
        
        resultado = MotorDeBusca.tratando_amazon(dados)
        produto = resultado[0]

        assert produto.preco == 1250.50

    def test_amazon_ignora_preco_zero(self):
        """Testando exclusão de Produtos com preço indisponíveis"""
        html_input = """
        <html>
            <h2>Produto Indisponível</h2>
            <!-- Sem tags de preço -->
        </html>
        """
        dados = [{"html": html_input}]
        
        resultado = MotorDeBusca.tratando_amazon(dados)
        
        assert len(resultado) == 0

    def test_amazon_link_absoluto(self):
        """Testa se links que já começam com http não ganham prefixo duplo"""
        html_input = """
        <html>
            <h2>
                <a href="https://www.amazon.com.br/oferta-do-dia">Produto Oferta</a>
            </h2>
            <span class="a-price"><span class="a-offscreen">R$ 10,00</span></span>
        </html>
        """
        dados = [{"html": html_input}]
        resultado = MotorDeBusca.tratando_amazon(dados)
        
        # Não deve ser "https://www.amazon.com.brhttps://*"
        assert resultado[0].link_produto == "https://www.amazon.com.br/oferta-do-dia"

    def test_amazon_moeda_dolar(self):
        """Testa a detecção de moeda quando o preço está em US$"""
        html_input = """
        <html>
            <h2>Importado</h2>
            <span class="a-price">
                <span class="a-offscreen">US$ 50.00</span>
            </span>
        </html>
        """
        dados = [{"html": html_input}]
        resultado = MotorDeBusca.tratando_amazon(dados)

        assert resultado[0].moeda == "$"
        assert resultado[0].preco == 50.00

    def test_amazon_vendas_ingles(self):
        """Testa a captura de vendas quando o site está em inglês ('bought')"""
        html_input = """
        <html>
            <h2>Produto Global</h2>
            <span class="a-price"><span class="a-offscreen">R$ 100,00</span></span>
            <span class="a-size-base a-color-secondary">5K+ bought in past month</span>
        </html>
        """
        dados = [{"html": html_input}]
        resultado = MotorDeBusca.tratando_amazon(dados)
        
        assert "5K+ bought" in resultado[0].numero_vendas

    def test_amazon_preco_com_simbolos_diferentes(self):
        """Testa o regex de limpeza para preços com caracteres não numéricos"""
        html_input = """
        <html>
            <h2>Produto Bugado</h2>
            <span class="a-price">
                <span class="a-offscreen">R$ 1.200,00 (Ofertasso!)</span>
            </span>
        </html>
        """
        dados = [{"html": html_input}]
        resultado = MotorDeBusca.tratando_amazon(dados)
        
        assert resultado[0].preco == 1200.00

    # ======================== 4. TESTES DE ORQUESTRAÇÃO DE FLUXO =================================
    
    @patch('buscaCrawler.motor_busca.MotorDeBusca.limpar_arquivos_temporarios')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.tratando_amazon')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.tratando_mercado_livre')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.carregar_dados_json')
    @patch('buscaCrawler.motor_busca.MercadoLivreCrawler')
    @patch('buscaCrawler.motor_busca.AmazonCrawler')
    def test_busca_metodo_completa(self, MockAmazonCrawler, MockMLCrawler, mock_carregar_json, mock_tratar_ml, mock_tratar_amazon, mock_limpar):
        """
        Testa o fluxo principal do método busca() usando Mocks
        Isolando: crawlers, leitura de arquivo e exclusão
        """
        termo_busca = "iphone"
        
        # Simulando retorno dos arquivos carregados (IO Mockado)
        # 1° chamada (Amazon), 2° chamada (Mercado Livre (ml))
        dados_fake_amazon = [{'html': '<html>Amazon Fake</html>'}]
        dados_fake_ml = [{'html': '<html>ML Fake</html>'}]
        mock_carregar_json.side_effect = [dados_fake_amazon, dados_fake_ml]

        # Simulando retorno do tratamento
        produto_fake_amz = MagicMock(spec=Produto)
        produto_fake_amz.nome = "iPhone Amazon Mockado"
        
        produto_fake_ml = MagicMock(spec=Produto)
        produto_fake_ml.nome = "iPhone ML Mockado"

        mock_tratar_amazon.return_value = [produto_fake_amz]
        mock_tratar_ml.return_value = [produto_fake_ml]

        resultado = MotorDeBusca.busca(termo_busca)

        # Verifica se os Crawlers foram instanciados e o método search foi chamado com os argumentos certos
        MockAmazonCrawler.return_value.search.assert_called() 
        MockMLCrawler.return_value.search.assert_called()
        
        # Verifica se tentou carregar os arquivos JSON
        self.assertEqual(mock_carregar_json.call_count, 2)
        
        # Verifica se os métodos de tratamento foram chamados repassando os dados corretos que vieram do "carregar"
        mock_tratar_ml.assert_called_once_with(dados_fake_ml)
        mock_tratar_amazon.assert_called_once_with(dados_fake_amazon)
        
        # Verifica se a limpeza foi chamada no final
        mock_limpar.assert_called_once()
        
        # Verifica se o resultado final é a soma das listas retornadas pelos mocks
        self.assertEqual(len(resultado), 2)
        self.assertIn(produto_fake_amz, resultado)
        self.assertIn(produto_fake_ml, resultado)

    # ======================== 5. TESTES DE FALHAS E TRATAMENTO DE ERROS ==========================

    @patch('buscaCrawler.motor_busca.MotorDeBusca.limpar_arquivos_temporarios')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.tratando_amazon')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.tratando_mercado_livre')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.carregar_dados_json')
    @patch('buscaCrawler.motor_busca.MercadoLivreCrawler')
    @patch('buscaCrawler.motor_busca.AmazonCrawler')
    def test_busca_com_json_vazio_ou_inexistente(self, MockAmazon, MockML, mock_carregar, mock_tratar_ml, mock_tratar_amz, mock_limpar):
        """
        Testando se o sistema não quebra e/ou retorna lista vazia
        """
        mock_carregar.side_effect = [[], []] 
        
        # Os tratadores recebem lista vazia e retornam lista vazia
        mock_tratar_ml.return_value = []
        mock_tratar_amz.return_value = []

        resultado = MotorDeBusca.busca("item inexistente")

        self.assertEqual(resultado, []) 
        mock_tratar_ml.assert_called_with([]) 
        mock_tratar_amz.assert_called_with([])
        mock_limpar.assert_called_once() 

    @patch('buscaCrawler.motor_busca.MotorDeBusca.limpar_arquivos_temporarios')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.tratando_amazon')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.tratando_mercado_livre')
    @patch('buscaCrawler.motor_busca.MotorDeBusca.carregar_dados_json')
    @patch('buscaCrawler.motor_busca.MercadoLivreCrawler')
    @patch('buscaCrawler.motor_busca.AmazonCrawler')
    def test_busca_fluxo_parcial_apenas_amazon_retorna(self, MockAmazon, MockML, mock_carregar, mock_tratar_ml, mock_tratar_amz, mock_limpar):
        """
        Testando se o resultado final contenha os produtos da Amazon
        """
        mock_carregar.side_effect = [[{'html': 'dado'}], []]

        produto_amz = MagicMock(spec=Produto)
        produto_amz.nome = "Kindle"
        
        mock_tratar_amz.return_value = [produto_amz] 
        mock_tratar_ml.return_value = []             

        resultado = MotorDeBusca.busca("kindle")

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].nome, "Kindle")

    @patch('buscaCrawler.motor_busca.os.remove') 
    @patch('buscaCrawler.motor_busca.glob.glob') 
    def test_limpeza_arquivos_com_erro_permissao(self, mock_glob, mock_os_remove):
        """
        Testa se o método 'limpar' captura o erro OSError com try/except e não trava o sistema
        """
        mock_glob.return_value = ['temp/arquivo1.json', 'temp/arquivo2.json']
        
        mock_os_remove.side_effect = [OSError("Permissão negada"), None]

        try:
            MotorDeBusca.limpar_arquivos_temporarios()
        except Exception as e:
            self.fail(f"O método limpar_arquivos_temporarios não tratou a exceção: {e}")

        self.assertEqual(mock_os_remove.call_count, 2)
        mock_os_remove.assert_has_calls([
            call('temp/arquivo1.json'),
            call('temp/arquivo2.json')
        ])

    @patch('buscaCrawler.motor_busca.AmazonCrawler')
    def test_busca_falha_crawler_explode(self, MockAmazonCrawler):
        """
        Teste em um cenário onde o crawler da Amazon lança uma exceção crítica.
        """
        MockAmazonCrawler.return_value.search.side_effect = Exception("Erro de Conexão")

        with self.assertRaises(Exception) as contexto:
            MotorDeBusca.busca("teste")
        
        self.assertIn("Erro de Conexão", str(contexto.exception))