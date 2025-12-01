class Produto():
    def __init__(self, loja:str, link_produto: str, nome:str, moeda:str, preco:float, frete:str, frete_gratis:bool, nota:float, numero_vendas: str, imagem: str):
        self.loja = loja
        self.link_produto = link_produto
        self.nome = nome
        self.moeda = moeda
        self.preco = preco
        self.frete = frete
        self.frete_gratis = frete_gratis
        self.nota = nota
        self.numero_vendas = numero_vendas
        self.imagem = imagem