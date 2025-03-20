from django.contrib import admin
from django.urls import path
from reservas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.reservar, name='reservar'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('gerenciar/', views.gerenciar_reservas, name='gerenciar_reservas'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva_cliente, name='cancelar_reserva_cliente'),
]
