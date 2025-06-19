from django.db import models
from django.contrib.auth.models import User
import uuid

class CodigoVerificacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.codigo}"


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    perfil = models.CharField(max_length=10, choices=[('comum', 'Comum'), ('master', 'Master')], default='comum')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.cpf}"