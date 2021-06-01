from apps import produtos
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core import paginator
from django.db.models import query
import unidecode, random #necessidade de instalar um pacote do unidecode
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.shortcuts import render, redirect, get_object_or_404
#importação para cadastrar os usuários
from django.contrib.auth.models import User
#importando modelos do app produtos
from produtos.models import * 
#importação para mensagens
from django.contrib import messages
#paginacao
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def meus_produtos(request):
        """Função que mostra as informações dos produtos que o usuário cadastrou"""
        if request.user.is_authenticated:
            id = request.user.id
            #produtos relacionados a uma pessoa especifica
            produtos = Produto.objects.order_by('-data_criacao').filter(pessoa=id)
            
            #caso o usuário acione, faz a busca de produtos
            if request.method == 'POST':
                produt_a_buscar = request.POST['nome_produto']
                produtos = produtos.filter(nome_produto__icontains=produt_a_buscar)
            #paginação de produtos
            paginator = Paginator(produtos, 3)
            page = request.GET.get('page')
            produtos_por_pagina = paginator.get_page(page)
            
            #usuarios
            usuarios_ultimos = User.objects.order_by('-date_joined')
            paginator2 = Paginator(usuarios_ultimos, 3)
            page2 = request.GET.get('page2')
            ultimos_usu = paginator2.get_page(page2)
            contextPro = { 
                'produtos': produtos_por_pagina,
                #tres ultimos usuarios
                'usuarios_ultimos': ultimos_usu,
            }
            return render (request, 'produtos/meus-produtos.html', contextPro)

def registrar_produtos(request):
    """Registrando produtos"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            #para gerar codigo aleatorio e único
            caracteres = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            numeros = list('123456789')
            tamanho = 6
            codigo = ''
            for x in range(tamanho):
                codigo += random.choice(caracteres+numeros)

            nome_produto = request.POST['nome_produto']
            email = request.POST['email']
            preco_produto = request.POST['preco']
            descricao_produto = request.POST['descricao']
            categoria_produto = request.POST['categoria']
            user = get_object_or_404(User, pk=request.user.id)
            slug = nome_produto.replace(" ","-")
            slug = unidecode.unidecode(slug).lower()
            
            # Verificando se o request FILES está vazio
            if 'foto_produto' in request.FILES:
                imagem_pro = request.FILES['foto_produto']
                produto = Produto.objects.create(pessoa=user, nome_produto=nome_produto,
                categoria=categoria_produto, imagem_produto=imagem_pro, descricao=descricao_produto, preco_produto=preco_produto, email=email, codigo=codigo, slug=slug)
            else:
                produto = Produto.objects.create(pessoa=user, nome_produto=nome_produto,
                categoria=categoria_produto, descricao=descricao_produto, preco_produto=preco_produto, email=email, codigo=codigo, slug=slug)
            produto.save()
            messages.success(request,  'Produto cadastrado com sucesso!')
            return redirect('meus_produtos')
        else:
            return render(request, 'produtos/registrar-produtos.html')
    else:
        return redirect('login')

def deletar_produto(request, produtinhos_id):
    """Deletando produtos do usuário especifico"""
    produto = get_object_or_404(Produto, pk=produtinhos_id)
    produto.delete()
    messages.success(request,'Produto deletado com sucesso!')
    return redirect('meus_produtos')

def editar_produto(request, produtinhos_id):
    produto = get_object_or_404(Produto, pk=produtinhos_id)
    context = {'produ':produto}
    return render(request, 'produtos/editar-produto.html' ,context)

def atualizar_produto(request, produtinhos_id):
    if request.method == 'POST':
        produto_id = request.POST['id_produto']
        p = Produto.objects.get(pk=produto_id)
        nome = request.POST['nome_produto']
        email = request.POST['email']
        descricao = request.POST['descricao']
        if not campo_vazio(nome):
            messages.error(request, 'O campo nome não pode ficar vazio!')
            return redirect('editar_produto', produtinhos_id)
        if not campo_vazio(email):
            messages.error(request, 'O campo email não pode ficar vazio!')
            return redirect('editar_produto', produtinhos_id) 
        if not campo_vazio(descricao):
            messages.error(request, 'O campo descrição não pode ficar vazio!')
            return redirect('editar_produto', produtinhos_id)  
        p.nome_produto = request.POST['nome_produto']
        p.email = request.POST['email']
        p.preco_produto = request.POST['preco']
        p.descricao = request.POST['descricao']
        p.categoria = request.POST['categoria']
        if 'foto_produto' in request.FILES:
            p.imagem_produto = request.FILES['foto_produto']
        p.save()
        messages.success(request, 'Produto editado com sucesso!')
        return redirect('meus_produtos')

def busca_produtos_dashboard(request):
    """Função que faz a busca de produtos no dashboard"""
    if request.user.is_authenticated:
        pesquisa_produto_dashboard = Produto.objects.order_by('-data_criacao')
        if request.method == 'GET':
            nome_a_buscar = request.GET['nome_busca']
            lista_produtos = pesquisa_produto_dashboard.filter(nome_produto__icontains=nome_a_buscar)
        #paginando
        paginator = Paginator(lista_produtos, 3)
        page = request.GET.get('page')
        produtos_por_pagina = paginator.get_page(page)
        qtd_produtos = len(pesquisa_produto_dashboard)
        pro_ultimo = Produto.objects.last()
        #usuarios
        usuarios_ultimos = User.objects.order_by('-date_joined')
        paginator2 = Paginator(usuarios_ultimos, 3)
        page2 = request.GET.get('page2')
        ultimos_usu = paginator2.get_page(page2)
        qua = len(usuarios_ultimos)
        
        contextDas = { 
                'produtos': produtos_por_pagina,
                'qtd':qtd_produtos,
                'pro_ulti': pro_ultimo,
                'qtd_usu': qua,
                #tres ultimos usuarios
                'usuarios_ultimos':ultimos_usu,
        }
        return render(request, 'usuarios/dashboard.html', contextDas)
    else:
        return redirect('login')

def campo_vazio(campo):
    return campo.strip()
