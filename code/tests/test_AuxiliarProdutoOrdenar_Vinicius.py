import pytest


from app.AuxiliarProduto.AuxiliarProduto import ordena_nota


def test_ordena_nota_ListaVazia():
    entrada = []
    esperado = []

    assert ordena_nota(entrada) == esperado

def test_ordena_nota_ListaOrdenadaCorreta():
    entrada = [
        ["Escudo Médio", "Loja de Proteção", "BRL", 1500, 30, 180, "url=escudo1", 4.8, 3, "importado", 3, False],
        ["Espada Foda", "Loja de Fodaongar", "BRL", 2000, 40, 220, "url=foda1", 4.9, 4, "nacional", 5, True],
        ["Poção de Vida", "Loja do Alquimista", "BRL", 500, 10, 50, "url=pocao1", 4.5, 10, "nacional", 1, True]
    ]
    
    esperado = [
        ["Espada Foda", "Loja de Fodaongar", "BRL", 2000, 40, 220, "url=foda1", 4.9, 4, "nacional", 5, True],
        ["Escudo Médio", "Loja de Proteção", "BRL", 1500, 30, 180, "url=escudo1", 4.8, 3, "importado", 3, False],
        ["Poção de Vida", "Loja do Alquimista", "BRL", 500, 10, 50, "url=pocao1", 4.5, 10, "nacional", 1, True]
    ]
    
    assert ordena_nota(entrada) == esperado
    
def test_ordena_nota_ListaCorrigeNota():
    entrada = [
        ["Escudo Médio", "Loja de Proteção", "BRL", 1500, 30, 180, "url=escudo1", 4.7, 3, "importado", 3, False],
        ["Espada Foda", "Loja de Fodaongar", "BRL", 2000, 40, 220, "url=foda1", 8.9, 4, "nacional", 50, True],
        ["Poção de Dor", "Loja do Alquimista", "BRL", 500, 10, 50, "url=pocao1", -1.5, 10, "nacional", 10, True]
    ]
    
    esperado = [
        ["Espada Foda", "Loja de Fodaongar", "BRL", 2000, 40, 220, "url=foda1", 5.0, 4, "nacional", 5, True],
        ["Escudo Médio", "Loja de Proteção", "BRL", 1500, 30, 180, "url=escudo1", 4.7, 3, "importado", 3, False],
        ["Poção de Dor", "Loja do Alquimista", "BRL", 500, 10, 50, "url=pocao1", 0, 10, "nacional", 10, True]
    ]
    
    assert ordena_nota(entrada) == esperado