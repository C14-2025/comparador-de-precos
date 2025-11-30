class Produto():
    def __init__(self, loja:str, nome:str, moeda:str, preco:float, frete:str, nota:float, numero_vendas:str):
        self.loja = loja
        self.nome = nome
        self.moeda = moeda
        self.preco = preco
        self.frete = frete
        self.nota = nota
        self.numero_vendas = numero_vendas

    def get_loja(self):
        return self.loja
    
    def get_nome(self):
        return self.nome
    
    def get_moeda(self):
        return self.moeda
    
    def get_preco(self):
        return self.preco
    
    def get_frete(self):
        return self.frete