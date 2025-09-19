import re
import requests

class Usuario:

    def __init__(self,nome,email,senha_hash,cep=None,idade=None,aniversario=None,nacionalidade=None,produtos_salvos=None):
        self.nome = nome
        self.email =  email
        self.senha_hash = senha_hash
        self.cep = cep
        self.idade = idade
        self.aniversario = aniversario
        self.nacionalidade = nacionalidade
        self.produtos_salvos = produtos_salvos if produtos_salvos is not None else [] # no começo, produtos salvos estará vazio

    def criar_conta(self):
            
        if not self.nome or not self.email or not self.senha_hash or not self.aniversario or not self.nacionalidade:
            raise ValueError("Dados obrigatorios incompletos")

        if self.cep:
            self.verificar_cep_valido()

        if self.idade is not None:
            if self.idade < 0 or self.idade > 120:
                raise ValueError("Idade invalida.")

    def verificar_cep_valido(self):
        
        match = re.match(r"^\d{5}-?\d{3}$", self.cep) # verifica se o valor inserido segue o padrão de cep/zip code

        if not match:
            raise ValueError("CEP invalido")
        else:
            self.cep = re.sub('-','',self.cep)

        cep_existe = requests.get(f"https://viacep.com.br/ws/{self.cep}/json")

        if cep_existe.json().get('erro') == True:
            raise ValueError("CEP inexistente")

            
            
    
        