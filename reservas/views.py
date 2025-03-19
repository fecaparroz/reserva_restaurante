from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Mesa, Reserva, ConfiguracaoRestaurante

def reservar(request):
    configuracao = ConfiguracaoRestaurante.objects.first()  # Carrega configuração global
    mesas_disponiveis = Mesa.objects.filter(disponivel=True)

    if request.method == "POST":
        nome_cliente = request.POST['nome']
        email_cliente = request.POST['email']
        quantidade_pessoas = int(request.POST['quantidade'])
        dia = request.POST['dia']
        periodo = request.POST['periodo']
        mesa_id = request.POST['mesa']

        mesa = Mesa.objects.get(id=mesa_id)

        # Verifica se ainda há capacidade disponível no restaurante
        total_reservado = sum(reserva.quantidade_pessoas for reserva in Reserva.objects.filter(dia=dia))
        if total_reservado + quantidade_pessoas > configuracao.total_pessoas:
            return render(request, "reservas/erro.html", {"mensagem": "Capacidade máxima do restaurante atingida."})

        try:
            reserva = Reserva(
                nome_cliente=nome_cliente,
                email_cliente=email_cliente,
                quantidade_pessoas=quantidade_pessoas,
                dia=dia,
                periodo=periodo,
                mesa=mesa,
            )
            reserva.clean()
            reserva.save()

            mesa.disponivel = False  # Atualiza status da mesa
            mesa.save()

            # Define horário limite para a reserva
            horario_limite = "12:30" if periodo == "almoço" else "19:30"

            return render(request, "reservas/sucesso.html", {
                "nome": nome_cliente,
                "mesa": mesa.numero,
                "dia": dia,
                "periodo": periodo,
                "horario_limite": horario_limite,
            })

        except ValidationError as e:
            return render(request, "reservas/erro.html", {"mensagem": str(e)})

    return render(request, "reservas/reservar.html", {"mesas": mesas_disponiveis})
