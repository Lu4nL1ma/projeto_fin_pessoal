import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login, logout
from app_fin_pessoal.models import receitas, categoria
from django.http import HttpResponseBadRequest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    # Renomeando os labels do formulário
    form.fields['username'].label = 'Usuário'
    form.fields['password'].label = 'Senha'
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona para a página de login após logout

@login_required
def home(request):
    lista_de_receitas = receitas.objects.all()
    por_pagina = 6  # Defina o número de receitas por página (ajuste conforme necessário)

    paginator = Paginator(lista_de_receitas, por_pagina)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'home.html', context)

def delete_receitas(request):
    if request.method == 'GET':
        ids_para_excluir = request.GET.get('ids')
        if ids_para_excluir:
            ids_list = ids_para_excluir.split(',')
            try:
                receitas.objects.filter(id__in=ids_list).delete()
                return redirect('home') # Redirecione para a página inicial após a exclusão
            except ValueError:
                return HttpResponseBadRequest("IDs inválidos.")
        else:
            return HttpResponseBadRequest("Nenhum ID fornecido para exclusão.")
    else:
        return HttpResponseBadRequest("Método inválido. Use GET para excluir.")

def form_receita(request):

    parcela = np.arange(1,49,1)

    categorias = categoria.objects.all()

    context = {'parcela': parcela, 'categorias': categorias}

    if request.method == 'POST':
        # Processar os dados do formulário enviados
        parcela = request.POST.get('parcela')
        tipo = request.POST.get('tipo')
        categori, natureza = request.POST.get('categoria').split('|')
        status = request.POST.get('status')
        fornecedor = request.POST.get('fornecedor')
        valor = request.POST.get('valor')
        previsao = request.POST.get('previsao')
        data_pagamento = request.POST.get('data_pagamento')
        
        #tratando dados da parcela
        parcela = int(parcela)

        if data_pagamento == "":
            data_pagamento = None
        else:
            data_pagamento = data_pagamento

        #lógica de repetição da parcela

        if parcela > 1:

            cont = 0

            while cont < parcela:

                previsao_final = datetime.strptime(previsao, '%Y-%m-%d') + relativedelta(months=cont)
                
                # Aqui você pode salvar os dados no seu modelo ou fazer qualquer outra ação necessária
                nova_receita = receitas(
                    tipo=tipo.title(),
                    status=status.title(),
                    natureza=natureza.title(),
                    fornecedor=fornecedor.title(),
                    categoria=categori,
                    valor=valor,
                    previsao=previsao_final,
                    data_pagamento=data_pagamento,
                    parcela=f'0{cont+1}/0{parcela}',
                    # descricao=descricao # Descomente se o seu model 'receitas' tiver um campo 'descricao'
                )
                
                nova_receita.save()

                cont = cont + 1

            return redirect('home')
        
        else:
            nova_receita = receitas(
            tipo=tipo,
            status=status,
            fornecedor=fornecedor,
            categori=categori,
            valor=valor,
            previsao=previsao,
            parcela=f'01/01',
            data_pagamento=data_pagamento,)
            
            nova_receita.save()

            return redirect('home')

    return render(request, 'form_receita.html', context)

def dashboard(request):

    #criando os valores unicos dos filtros
    fornecedor = receitas.objects.values_list('fornecedor', flat=True).distinct()

    #filtrando dados do df
    campos = ['tipo', 'natureza', 'status', 'fornecedor', 'parcela', 'categoria','valor', 'previsao', 'data_pagamento']
    
    data = receitas.objects.all().values_list(*campos)

    df = pd.DataFrame(data, columns=campos)

    despesa_total = df[df['tipo'] == 'Despesa']['valor'].sum()

    receita_total = df[df['tipo'] == 'Receita']['valor'].sum()

    print(despesa_total)

    context = {'fornecedor': fornecedor,'despesa_total': despesa_total, 'receita_total': receita_total}

    return render(request, 'dashboard.html', context)

