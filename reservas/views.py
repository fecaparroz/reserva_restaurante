from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Mesa, Reserva

def reservar(request):
    # Busca mesas disponíveis
    mesas_disponiveis = Mesa.objects.filter(disponivel=True)
    
    # Calcula o total de pessoas já reservadas
    reservas_existentes = Reserva.objects.all()
    total_pessoas_reservadas = sum(reserva.quantidade_pessoas for reserva in reservas_existentes)

    if request.method == "POST":
        nome_cliente = request.POST.get('nome')
        email_cliente = request.POST.get('email')
        quantidade_pessoas = int(request.POST.get('quantidade', 0))
        dia_str = request.POST.get('dia')
        periodo = request.POST.get('periodo')

        # Validação para garantir que há capacidade disponível
        if not mesas_disponiveis.exists():
            return render(request, "reservas/erro.html", {"mensagem": "Desculpe, todas as mesas estão reservadas."})
        
        if total_pessoas_reservadas + quantidade_pessoas > 100:
            return render(request, "reservas/erro.html", {"mensagem": "Desculpe, a capacidade máxima do restaurante foi atingida."})

        try:
            # Converte a string de data para objeto date
            dia = datetime.strptime(dia_str, '%Y-%m-%d').date()
            
            # Verifica se é domingo
            if dia.weekday() == 6:
                return render(request, "reservas/erro.html", {"mensagem": "O restaurante está fechado aos domingos."})
            
            # Atribui a primeira mesa disponível com capacidade suficiente
            mesa = None
            for m in mesas_disponiveis:
                if m.capacidade >= quantidade_pessoas:
                    # Verifica se esta mesa já está reservada para este dia e período
                    if not Reserva.objects.filter(mesa=m, dia=dia, periodo=periodo).exists():
                        mesa = m
                        break
            
            if not mesa:
                return render(request, "reservas/erro.html", {"mensagem": "Não há mesas disponíveis com capacidade suficiente para o número de pessoas informado."})

            # Cria a reserva
            reserva = Reserva(
                nome_cliente=nome_cliente,
                email_cliente=email_cliente,
                quantidade_pessoas=quantidade_pessoas,
                dia=dia,
                periodo=periodo,
                mesa=mesa,
            )
            
            # Valida e salva
            reserva.clean()
            reserva.save()

            # Define horário limite para a reserva
            horario_limite = "12:30" if periodo == "almoço" else "19:30"

            return render(request, "reservas/sucesso.html", {
                "nome": nome_cliente,
                "mesa": mesa.numero,
                "dia": dia.strftime('%d/%m/%Y'),  # Formato brasileiro
                "periodo": periodo,
                "horario_limite": horario_limite,
            })

        except ValidationError as e:
            return render(request, "reservas/erro.html", {"mensagem": str(e)})
        except ValueError as e:
            return render(request, "reservas/erro.html", {"mensagem": "Formato de data inválido."})

    return render(request, "reservas/reservar.html")

def sucesso(request):
    return render(request, "reservas/sucesso.html")
