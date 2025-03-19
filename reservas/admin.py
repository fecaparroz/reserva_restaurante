from django.contrib import admin
from .models import Mesa, Reserva, ConfiguracaoRestaurante

@admin.register(ConfiguracaoRestaurante)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('total_mesas', 'total_pessoas')

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidade', 'disponivel')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'quantidade_pessoas', 'dia', 'periodo', 'mesa')
