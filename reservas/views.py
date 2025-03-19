from django.shortcuts import render, redirect
from .models import Mesa, Reserva

# Página para reservar mesas
def reservar(request):
    # Busca todas as mesas disponíveis
    mesas_disponiveis = Mesa.objects.filter(disponivel=True)

    if request.method == "POST":
        # Captura os dados enviados pelo formulário
        nome_cliente = request.POST['nome']
        email_cliente = request.POST['email']
        mesa_id = request.POST['mesa']
        data = request.POST['data']
        horario = request.POST['horario']

        # Busca a mesa selecionada
        mesa = Mesa.objects.get(id=mesa_id)

        # Cria a reserva no banco de dados
        Reserva.objects.create(
            nome_cliente=nome_cliente,
            email_cliente=email_cliente,
            mesa=mesa,
            data=data,
            horario=horario,
        )

        # Atualiza o status da mesa para "indisponível"
        mesa.disponivel = False
        mesa.save()

        # Redireciona para a página de sucesso
        return redirect('sucesso')

    # Renderiza a página com as mesas disponíveis
    return render(request, "reservar.html", {'mesas': mesas_disponiveis})

# Página de confirmação de reserva
def sucesso(request):
    return render(request, "sucesso.html")
