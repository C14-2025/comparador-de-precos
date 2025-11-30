from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=200)
    cep = models.CharField(max_length=9)
    nacionalidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
