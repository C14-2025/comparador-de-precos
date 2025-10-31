class Usuario:

    def __init__(self,nome,email,senha_hash,cep=None,idade=None,aniversario=None,nacionalidade=None,produtos_salvos=None):
        self.nome = nome
        self.email =  email
        self.senha_hash = senha_hash
        self.cep = cep
        self.nacionalidade = nacionalidade
        self.produtos_salvos = produtos_salvos if produtos_salvos is not None else [] # no começo, produtos salvos estará vazio

    def criar_conta(self):
            
        if not self.nome or not self.email or not self.senha_hash or not self.nacionalidade:
            raise ValueError("Dados obrigatorios incompletos")



            
            
    
        