

# Create your models here.
from django.db import models

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidade = models.IntegerField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.numero}"

class Reserva(models.Model):
    nome_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()

    def __str__(self):
        return f"{self.nome_cliente} - Mesa {self.mesa.numero}"
