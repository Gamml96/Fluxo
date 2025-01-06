from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Receita(models.Model):
    id_receita = models.AutoField(primary_key=True)
    data = models.DateField(default=timezone.now)
    conta = models.TextField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.TextField(max_length=100)
    observacao = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Associando a Receita a um usuário

class Despesa(models.Model):
    id_despesa = models.AutoField(primary_key=True)
    data = models.DateField(default=timezone.now)
    tipo = models.TextField(max_length=100,default='Crédito')
    conta = models.TextField(max_length=100)
    vencimento = models.DateField(default=timezone.now)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.TextField(max_length=100)
    observacao = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Associando a Despesa a um usuário

class Contas(models.Model):
    id_conta = models.AutoField(primary_key=True)
    conta = models.TextField(max_length=100)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.TextField(max_length=2)
    data_fechamento = models.TextField(max_length=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Associando a Conta a um usuário

class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    categoria = models.TextField(max_length=100)
    tipo_categoria = models.TextField(max_length=100)    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Associando a Categoria a um usuário
