from django.contrib import admin
from django.urls import path
from reservas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.reservar, name='reservar'),
    path('sucesso/', views.sucesso, name='sucesso'),
]
