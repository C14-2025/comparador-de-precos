import requests

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
    

    # Converte o valor do produto na sua moeda local para BRL (Real) usando uma api que retorna um json
    # que possui o valor de 1 unidade dessa moeda nas demais moedas do mundo, no caso, pegamos o valor em brl
    # e só multiplicamos para poder fazer a conversão
    def converter_preco(self):  
        print(self.moeda + f" {self.valor}")
        json_moeda = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{self.moeda}.json").json()
        real_na_moeda = json_moeda[self.moeda]['brl']
        valor_convertido = self.valor * real_na_moeda
        print(f"R$ {valor_convertido}")
        return valor_convertido
    
    # Caso tenha valor de frete ele vai ser calculado nessa função
    # TODO: Adicionar verificação pra ver se precisa converter a moeda ou não, ai seria só chamar a função acima
    def somar_valor(self):
        self.valor_total = self.valor + self.frete

