import pytest

from app.busca.MotorDeBusca import MonitorDeBusca

def test_catalogo_completo_caminho_errado():
    log_saida = ""
    with pytest.raises(FileNotFoundError):
        log_saida = MonitorDeBusca.catalogo_completo("caminho/que/nao/existe.csv")

    assert len(log_saida) == 0

def test_catalogo_completo_caminho_valido():
    log_saida = ""
    log_saida = MonitorDeBusca.catalogo_completo("tests/data/produtos.csv")
    assert len(log_saida) > 0

def test_catalogo_buscando_produto_faltante():
    log_saida = MonitorDeBusca.busca_produto(nome_produto="XXXXXXXXXX", arquivo="tests/data/produtos.csv")
    assert log_saida == "Nenhum Produto Com Esse Nome Encontrado!!!"

def test_catalogo_buscando_produto_existente():
    log_saida = ""
    log_saida = MonitorDeBusca.busca_produto(nome_produto="SmarTphoNe", arquivo='tests/data/produtos.csv')
    log_saida = str(log_saida)
    assert "Smartphone Modelo X".lower() in log_saida.lower()