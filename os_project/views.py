from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Cliente, OrdemServico, Tecnico
from .forms import OrdemServicoForm, ClienteForm, TecnicoForm, HomeSearchForm, ClienteSearchForm, TecnicoSearchForm, CriarOSForm, AlterarOSForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q

def home(request):
    form = HomeSearchForm(request.GET or None)
    ordens_servico = []

    query = """
        SELECT 
            ordem_servico_id, data_criacao, hora_criacao, data_termino, hora_termino, status,
            cliente_id, cliente_nome, tecnico_id, tecnico_nome
        FROM 
            home_os
    """

    if form.is_valid():
        search_field = form.cleaned_data.get('search_field')
        search_option = form.cleaned_data.get('search_option')
        search_date = form.cleaned_data.get('search_date')
        search_time = form.cleaned_data.get('search_time')

        if search_option == 'os':
            query += f" WHERE ordem_servico_id LIKE '%{search_field}%'"
        elif search_option == 'cliente_id':
            query += f" WHERE cliente_id LIKE '%{search_field}%'"
        elif search_option == 'cliente_nome':
            query += f" WHERE cliente_nome LIKE '%{search_field}%'"
        elif search_option == 'data_criacao' and search_date:
            query += f" WHERE data_criacao = '{search_date}'"
        elif search_option == 'hora_criacao' and search_time:
            query += f" WHERE hora_criacao = '{search_time}'"
        elif search_option == 'data_termino' and search_date:
            query += f" WHERE data_termino = '{search_date}'"
        elif search_option == 'hora_termino' and search_time:
            query += f" WHERE hora_termino = '{search_time}'"
        elif search_option == 'status':
            query += f" WHERE status LIKE '%{search_field}%'"
        elif search_option == 'tecnico_id':
            query += f" WHERE tecnico_id LIKE '%{search_field}%'"
        elif search_option == 'tecnico_nome':
            query += f" WHERE tecnico_nome LIKE '%{search_field}%'"

    with connection.cursor() as cursor:
        cursor.execute(query)
        ordens_servico = cursor.fetchall()

    context = {
        'form': form,
        'ordens_servico': ordens_servico
    }

    return render(request, 'home.html', context)

@require_POST
def atualizar_status(request, os_id):
    ordem_servico = get_object_or_404(OrdemServico, id=os_id)
    novo_status = request.POST.get('status')

    if novo_status in ['aberto', 'concluido', 'pendente']:
        ordem_servico.status = novo_status
        ordem_servico.save()
        messages.success(request, 'Status atualizado com sucesso!')
    else:
        messages.error(request, 'Status inválido.')

    return redirect('detalhes_os', os_id=os_id)

def criar_os(request):
    if request.method == 'POST':
        form = CriarOSForm(request.POST)
        if form.is_valid():
            ordem_servico = form.save(commit=False)
            ordem_servico.status = 'aberto'
            ordem_servico.save()
            messages.success(request, 'Ordem de Serviço criada com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao criar Ordem de Serviço. Verifique os campos obrigatórios.')
    else:
        form = CriarOSForm()

    clientes = Cliente.objects.all()
    tecnicos = Tecnico.objects.all()

    return render(request, 'criar_os.html', {'form': form, 'clientes': clientes, 'tecnicos': tecnicos})

def detalhes_os(request, os_id):
    ordem_servico = get_object_or_404(OrdemServico, id=os_id)
    return render(request, 'detalhes_os.html', {'ordem_servico': ordem_servico})

def alterar_os(request, os_id):
    ordem_servico = get_object_or_404(OrdemServico, id=os_id)
    if request.method == 'POST':
        form = AlterarOSForm(request.POST, request.FILES, instance=ordem_servico)
        if form.is_valid():
            ordem_servico = form.save(commit=False)
            ordem_servico.save()
            messages.success(request, 'Ordem de serviço atualizada com sucesso!')
            return redirect('detalhes_os', os_id=os_id)
    else:
        form = AlterarOSForm(instance=ordem_servico)

    clientes = Cliente.objects.all()
    tecnicos = Tecnico.objects.all()

    return render(request, 'alterar_os.html', {'form': form, 'clientes': clientes, 'tecnicos': tecnicos, 'ordem_servico': ordem_servico})

def excluir_os(request, os_id):
    ordem_servico = get_object_or_404(OrdemServico, id=os_id)
    if request.method == 'POST':
        ordem_servico.delete()
        messages.success(request, 'Ordem de serviço excluída com sucesso!')
        return redirect('home')
    return render(request, 'detalhes_os.html', {'ordem_servico': ordem_servico})

def cadastro_cliente(request, id=None):
    if id:
        cliente = get_object_or_404(Cliente, id=id)
    else:
        cliente = Cliente()
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            if id:
                messages.success(request, 'Cliente atualizado com sucesso!')
            else:
                messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('home')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cadastro_cliente.html', {'form': form, 'cliente': cliente})

def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('home')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'detalhes_cliente.html', {'form': form, 'cliente': cliente})

def buscar_cliente(request):
    query = request.GET.get('query', '')
    clientes = Cliente.objects.filter(Q(nome__icontains=query) | Q(id__icontains(query)))
    data = [{'id': cliente.id, 'nome': cliente.nome, 'rua': cliente.rua, 'telefone': cliente.telefone, 'email': cliente.email} for cliente in clientes]
    return JsonResponse(data, safe=False)

def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('lista_clientes')
    return render(request, 'detalhes_cliente.html', {'cliente': cliente})

def cadastro_tecnico(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            tecnico = form.save()
            messages.success(request, f'Técnico {tecnico.nome_completo} cadastrado com sucesso!')
            return redirect('home')
    else:
        form = TecnicoForm()
    return render(request, 'cadastro_tecnico.html', {'form': form})

def detalhes_tecnico(request, id):
    tecnico = get_object_or_404(Tecnico, id=id)
    if request.method == 'POST':
        form = TecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Técnico atualizado com sucesso!')
            return redirect('home')
    else:
        form = TecnicoForm(instance=tecnico)
    return render(request, 'detalhes_tecnico.html', {'form': form, 'tecnico': tecnico})

def buscar_tecnico(request):
    query = request.GET.get('query', '')
    tecnicos = Tecnico.objects.filter(Q(nome_completo__icontains=query) | Q(id__icontains(query)))
    data = [{'id': tecnico.id, 'nome_completo': tecnico.nome_completo} for tecnico in tecnicos]
    return JsonResponse(data, safe=False)

def excluir_tecnico(request, id):
    tecnico = get_object_or_404(Tecnico, id=id)
    if request.method == 'POST':
        tecnico.delete()
        messages.success(request, 'Técnico excluído com sucesso!')
        return redirect('lista_tecnicos')
    return render(request, 'detalhes_tecnico.html', {'tecnico': tecnico})

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro_usuario.html', {'form': form})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def lista_tecnicos(request):
    tecnicos = Tecnico.objects.all()
    return render(request, 'lista_tecnicos.html', {'tecnicos': tecnicos})
