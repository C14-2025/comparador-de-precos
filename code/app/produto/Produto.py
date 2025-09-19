class Produto:
    def __init__(self, nome, moeda, valor, frete, link, nota, estoque, tipo_envio, cupom):
        if valor < 0:
            raise ValueError("O valor do produto não pode ser negativo")
        
        self.nome = nome
        #adicionar o objeto loja depois
        self.moeda = moeda
        self.valor = valor 
        self.frete = frete
        self.valor_total = 0
        self.link = link
        self.nota = nota
        self.estoque = estoque
        self.tipo_envio = tipo_envio
        #adicionar tempo_entrega depois
        self.cupom = cupom
        pass
    

    # A conversão da moeda local do produto para Real vai ser feita de outra forma futuramente
    # Por hora para fins de teste ela está dessa forma
    def converter_preco(self, valor_moeda_em_real, valor_na_moeda):
        print(self.moeda + f"${valor_na_moeda}")
        valor_convertido = valor_moeda_em_real * valor_na_moeda
        print(f"R$ {valor_convertido}")
        return valor_convertido
    
    # Caso tenha valor de frete ele vai ser calculado nessa função
    # TODO: Adicionar verificação pra ver se precisa converter a moeda ou não, ai seria só chamar a função acima
    def somar_valor(self):
        self.valor_total = self.valor + self.frete
