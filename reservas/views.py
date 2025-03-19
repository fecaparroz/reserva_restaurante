from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from .models import Mesa, Reserva, ConfiguracaoRestaurante

def reservar(request):
    # Obtém a configuração do restaurante
    config = ConfiguracaoRestaurante.objects.first()
    if not config:
        config = ConfiguracaoRestaurante.objects.create(capacidade_pessoas=20, capacidade_mesas=3)  # Valores reduzidos para teste
    
    # Busca mesas disponíveis
    mesas_disponiveis = Mesa.objects.filter(disponivel=True)
    
    if request.method == "POST":
        nome_cliente = request.POST.get('nome')
        email_cliente = request.POST.get('email')
        quantidade_pessoas = int(request.POST.get('quantidade', 0))
        dia_str = request.POST.get('dia')
        periodo = request.POST.get('periodo')
        
        try:
            # Converte a string de data para um objeto date
            dia = datetime.strptime(dia_str, '%Y-%m-%d').date()
            
            # Verifica se é domingo
            if dia.weekday() == 6:
                return render(request, "reservas/erro.html", {"mensagem": "O restaurante está fechado aos domingos."})
            
            # Verifica se o cliente já tem uma reserva
            if Reserva.objects.filter(email_cliente=email_cliente).exists():
                return render(request, "reservas/erro.html", {"mensagem": "Você já possui uma reserva. Limite de 1 reserva por email."})
            
            # Calcula o total de pessoas e mesas já reservadas para este dia e período
            reservas_dia_periodo = Reserva.objects.filter(dia=dia, periodo=periodo)
            total_pessoas_reservadas = sum(reserva.quantidade_pessoas for reserva in reservas_dia_periodo)
            total_mesas_reservadas = reservas_dia_periodo.count()
            
            # Verifica se há capacidade disponível para este dia e período
            if total_pessoas_reservadas + quantidade_pessoas > config.capacidade_pessoas:
                return render(request, "reservas/erro.html", {"mensagem": "Desculpe, a capacidade máxima de pessoas para este dia e período foi atingida."})
            
            if total_mesas_reservadas >= config.capacidade_mesas:
                return render(request, "reservas/erro.html", {"mensagem": "Desculpe, todas as mesas para este dia e período já estão reservadas."})
            
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

@login_required
def gerenciar_reservas(request):
    hoje = timezone.now().date()
    
    # Filtrar reservas por dia (padrão: hoje)
    dia_filtro = request.GET.get('dia', hoje.strftime('%Y-%m-%d'))
    try:
        dia_filtro = datetime.strptime(dia_filtro, '%Y-%m-%d').date()
    except ValueError:
        dia_filtro = hoje
    
    # Obter reservas do dia filtrado
    reservas_almoco = Reserva.objects.filter(dia=dia_filtro, periodo='almoço').order_by('mesa__numero')
    reservas_jantar = Reserva.objects.filter(dia=dia_filtro, periodo='jantar').order_by('mesa__numero')
    
    # Calcular estatísticas
    total_pessoas_almoco = sum(r.quantidade_pessoas for r in reservas_almoco)
    total_pessoas_jantar = sum(r.quantidade_pessoas for r in reservas_jantar)
    
    # Obter configuração
    config = ConfiguracaoRestaurante.objects.first()
    if not config:
        config = ConfiguracaoRestaurante.objects.create(capacidade_pessoas=20, capacidade_mesas=3)
    
    # Cancelar reserva se solicitado
    if request.method == 'POST' and 'cancelar_reserva' in request.POST:
        reserva_id = request.POST.get('reserva_id')
        try:
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.delete()
            return redirect('gerenciar_reservas')
        except Reserva.DoesNotExist:
            pass
    
    context = {
        'dia_filtro': dia_filtro,
        'reservas_almoco': reservas_almoco,
        'reservas_jantar': reservas_jantar,
        'total_pessoas_almoco': total_pessoas_almoco,
        'total_pessoas_jantar': total_pessoas_jantar,
        'config': config,
        'hoje': hoje,
    }
    
    return render(request, 'reservas/gerenciar_reservas.html', context)
