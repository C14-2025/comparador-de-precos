import re
from Usuario import Usuario
'''
deixando isso aq comentado só por via das duvidas

regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[;:.><,!@#$%¨&*_=+~'^-])[a-zA-Z0-9;:.><,!@#$%¨&*_=+~'^-]{12,}$"
txt1 = "!EuvoumataroJohn69~"

x = re.findall(regex, txt1)
print(x)

if re.fullmatch(regex,txt1):
    print("Senha válida!")
else:
    print("Senha inválida!")
'''

class Cadastro:
    def __init__(self):
        self.regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[;:.><,!@#$%¨&*_=+~'^-])[a-zA-Z0-9;:.><,!@#$%¨&*_=+~'^-]{12,}$"
        pass

    def __verifica_senha_forte(self,senha):
        if re.fullmatch(self.regex, senha):
            print("Senha válida!")
            return True
        else:
            print("Senha inválida!")
            return False

    def cadastrar(self, nome, email, senha):
        if self.__verifica_senha_forte(senha):
            usuario = Usuario(nome, email, senha)
            return usuario
        else:
            print("Garanta que sua senha tenha pelo menos 12 caracteres, uma letra minuscula, uma letra maiuscula, um numero e um caracter especial")
