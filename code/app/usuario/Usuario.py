import re

class Usuario:

    def __init__(self,nome,email,senha_hash,cep=None,idade=None,aniversario=None,nacionalidade=None,produtos_salvos=None):
        self.__nome = nome
        self.__email =  email
        self.__senha_hash = senha_hash
        self.__cep = cep
        self.__idade = idade
        self.__aniversario = aniversario
        self.__nacionalidade = nacionalidade
        self.__produtos_salvos = produtos_salvos if produtos_salvos is not None else [] # no começo, produtos salvos estará vazio

    def criar_conta(self):
        try:
            if not self.__nome or not self.__email or not self.__senha_hash or not self.__aniversario or not self.__nacionalidade:
                raise ValueError("Dados obrigatorios incompletos")

            if self.__cep:
                self.verificar_cep_valido()

            if self.__idade is not None:
                if self.__idade < 0 or self.__idade > 120:
                    raise ValueError("Idade invalida.")

        except Exception as e:
            return "Erro ao criar conta"

    def verificar_cep_valido(self):
        try:
            match = re.match(r"^\d{5}-?\d{3}$", self.__cep) # verifica se o valor inserido segue o padrão de cep/zip code

            if not match:
                raise ValueError("CEP invalido")

        except Exception as e:
            return "Cep invalido"

            
            
    
        