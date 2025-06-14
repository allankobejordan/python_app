# produtos/models.py

from django.db import models

class Produto(models.Model):
    TAMANHOS = [
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
    ]

    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=200, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tamanho = models.CharField(max_length=2, choices=TAMANHOS, default='M')
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    def __str__(self):
        return self.nome
