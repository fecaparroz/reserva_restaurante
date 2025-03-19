from django.shortcuts import render, redirect
from .models import Mesa, Reserva

def reservar(request):
    mesas_disponiveis = Mesa.objects.filter(disponivel=True)

    if request.method == "POST":
        nome_cliente = request.POST['nome']
        email_cliente = request.POST['email']
        mesa_id = request.POST['mesa']
        data = request.POST['data']
        horario = request.POST['horario']

        mesa = Mesa.objects.get(id=mesa_id)

        Reserva.objects.create(
            nome_cliente=nome_cliente,
            email_cliente=email_cliente,
            mesa=mesa,
            data=data,
            horario=horario,
        )

        mesa.disponivel = False
        mesa.save()

        return redirect('sucesso')

    return render(request, "reservas/reservar.html", {'mesas': mesas_disponiveis})

def sucesso(request):
    return render(request, "reservas/sucesso.html")
