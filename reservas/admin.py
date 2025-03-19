from django.contrib import admin
from .models import Mesa, Reserva

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
