from rest_framework import serializers

class ProdutoSerializer(serializers.Serializer):
    loja = serializers.CharField()
    link_produto = serializers.CharField()
    nome = serializers.CharField()
    moeda = serializers.CharField()
    preco = serializers.FloatField()
    frete = serializers.CharField()
    frete_gratis = serializers.BooleanField()
    nota = serializers.FloatField()
    numero_vendas = serializers.CharField()
    imagem = serializers.CharField()
