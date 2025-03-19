from django.db import models
from django.core.exceptions import ValidationError

class ConfiguracaoRestaurante(models.Model):
    total_pessoas = models.IntegerField(default=100)  # Capacidade máxima
    total_mesas = models.IntegerField(default=30)     # Número total de mesas

    def __str__(self):
        return f"{self.total_mesas} mesas, {self.total_pessoas} pessoas"

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidade = models.IntegerField(default=10)  # Máximo de pessoas por mesa
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.numero}"

class Reserva(models.Model):
    nome_cliente = models.CharField(max_length=100)
    quantidade_pessoas = models.IntegerField()
    dia = models.DateField()
    periodo = models.CharField(max_length=10, choices=[('almoço', 'Almoço'), ('jantar', 'Jantar')])
    email_cliente = models.EmailField()
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)

    def clean(self):
        # Validação para não permitir reservas aos domingos
        if self.dia.weekday() == 6:
            raise ValidationError("O restaurante está fechado aos domingos.")
        # Validação para garantir que a quantidade de pessoas não ultrapasse o limite
        if self.quantidade_pessoas > self.mesa.capacidade:
            raise ValidationError(f"A mesa suporta no máximo {self.mesa.capacidade} pessoas.")

    def __str__(self):
        return f"{self.nome_cliente} ({self.quantidade_pessoas} pessoas) - {self.periodo} na Mesa {self.mesa.numero}"
