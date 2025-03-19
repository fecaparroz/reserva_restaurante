from django.contrib import admin
from .models import Mesa, Reserva, ConfiguracaoRestaurante

@admin.register(ConfiguracaoRestaurante)
class ConfiguracaoRestauranteAdmin(admin.ModelAdmin):
    list_display = ('capacidade_pessoas', 'capacidade_mesas')
    fieldsets = (
        ('Capacidade do Restaurante', {
            'fields': ('capacidade_pessoas', 'capacidade_mesas'),
            'description': 'Configure a capacidade máxima do restaurante por período (almoço/jantar)'
        }),
    )

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidade', 'disponivel')
    list_filter = ('disponivel', 'capacidade')
    search_fields = ('numero',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'email_cliente', 'quantidade_pessoas', 'dia', 'periodo', 'mesa')
    list_filter = ('dia', 'periodo')
    search_fields = ('nome_cliente', 'email_cliente')
    date_hierarchy = 'dia'
