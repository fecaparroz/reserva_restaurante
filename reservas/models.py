from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

class ConfiguracaoRestaurante(models.Model):
    capacidade_pessoas = models.IntegerField(default=20)  # Reduzido para 20 para testes
    capacidade_mesas = models.IntegerField(default=3)     # Reduzido para 3 para testes
    
    def __str__(self):
        return f"Configuração: {self.capacidade_mesas} mesas, {self.capacidade_pessoas} pessoas"

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidade = models.IntegerField(default=10)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.numero} (capacidade: {self.capacidade})"

class Reserva(models.Model):
    nome_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    quantidade_pessoas = models.IntegerField()
    dia = models.DateField()
    periodo = models.CharField(max_length=10, choices=[('almoço', 'Almoço'), ('jantar', 'Jantar')])
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)

    def clean(self):
        # Converte o campo 'dia' para um objeto datetime.date se for string
        if isinstance(self.dia, str):
            try:
                self.dia = datetime.strptime(self.dia, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Formato de data inválido. Use YYYY-MM-DD.")

        # Validação: Não permite reservas aos domingos
        if self.dia.weekday() == 6:  # Domingo é representado por 6
            raise ValidationError("O restaurante está fechado aos domingos.")

        # Validação: Garante que a quantidade de pessoas não excede a capacidade da mesa
        if self.quantidade_pessoas > self.mesa.capacidade:
            raise ValidationError(f"A mesa suporta no máximo {self.mesa.capacidade} pessoas.")
            
        # Validação: Limite de 1 reserva por email
        if Reserva.objects.filter(email_cliente=self.email_cliente).exclude(id=self.id).exists():
            raise ValidationError("Você já possui uma reserva. Limite de 1 reserva por email.")

    def __str__(self):
        return f"{self.nome_cliente} - {self.quantidade_pessoas} pessoas - {self.periodo} - Mesa {self.mesa.numero}"
