# sistema/anuncio/models.py

from django.db import models
from veiculo.models import Veiculo
from django.contrib.auth.models import User
from .consts import OPCOES_STATUS

class Anuncio(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quilometragem = models.PositiveIntegerField()
    telefone = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    status = models.CharField(max_length=10, choices=OPCOES_STATUS, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo