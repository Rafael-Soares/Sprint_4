from django.core import paginator
from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import get_object_or_404, render, redirect
#importação para cadastrar os usuários
from django.contrib.auth.models import User
#importação para autenticacao dos usuarios e mensagens
from django.contrib import auth, messages
#importando modelos do app produtos
from produtos.models import *
from .models import *
from django.core.paginator import Paginator 

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        #validações
        if not campo_vazio(username):
            messages.error(request, 'O campo username não pode ficar vazio')
            return redirect('login')
        if not campo_vazio(senha):
            messages.error(request, 'O campo senha não pode ficar vazio')
            return redirect('login')
        if User.objects.filter(username=username).exists(): #verificando se o username existe
            user = auth.authenticate(request, username=username, password=senha)    
            if user is not None: #autenticacao
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('dashboard')         
            else:
                messages.error(request,'Email ou senha inválidos')
                return redirect('login')
        else:
            messages.error(request, 'O usuário não existe')
            return redirect('login')
    else:
        return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def cadastro(request):
    if request.method == 'POST':
        email = request.POST['email']
        nome_pri = request.POST['nome_primeiro']
        nome_seg = request.POST['nome_segundo']
        username = request.POST['username']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']
    #validações
        if not campo_vazio(email):
            messages.error(request, 'O campo email não pode ficar vazio')
            return redirect('cadastro')
        if not campo_vazio(nome_pri):
            messages.error(request, 'O campo nome não pode ficar vazio')
            return redirect('cadastro')
        if not campo_vazio(nome_seg):
            messages.error(request, 'O campo nome não pode ficar vazio')
            return redirect('cadastro')
        if not campo_vazio(username):
            messages.error(request, 'O campo username não pode ficar vazio')
            return redirect('cadastro')
        if not campo_vazio(senha):
            messages.error(request, 'O campo senha não pode ficar vazio')
            return redirect('cadastro')
        if not campo_vazio(senha2):
            messages.error(request, 'O campo confirmação de senha não pode ficar vazio')
            return redirect('cadastro')
        if senha_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():  #verificando se o usuário já existe pelo email
            messages.error(request, 'Usuário já cadastrado!')
            return redirect ('cadastro')
        if User.objects.filter(username=username).exists(): #verificando se o usuário já existe pelo username
            messages.error(request, 'Usuário já cadastrado!')
            return redirect('cadastro')
        user = User.objects.create_user(username=username, email=email, password=senha, first_name=nome_pri, last_name=nome_seg) #cadastrando usuário
        user.save()
        imagem_user = Usuario.objects.create(pessoa=user)
        imagem_user.save()
        messages.success(request,  'Cadastro realizado com sucesso!')
        return redirect('login')
    else:   
        return render(request, 'usuarios/cadastro.html')

def dashboard(request):
    if request.user.is_authenticated:
        #produtos
        produtos = Produto.objects.order_by('-data_criacao')
        paginator = Paginator(produtos, 3)
        page = request.GET.get('page')
        produtos_por_pagina = paginator.get_page(page)
        qtd_produtos = len(produtos)
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
       
def usuarios(request):
        #Ultimos cadastrados
        usuarios_ultimos = User.objects.order_by('-date_joined')
        paginator2 = Paginator(usuarios_ultimos, 3)
        page2 = request.GET.get('page2')
        ultimos_usu = paginator2.get_page(page2)
        
        # Usuarios na paginaçao
        usuarios = User.objects.order_by('-date_joined')
        #realizando a busca
        if request.method == 'GET':
            nome = request.GET['nome_usuario']
            usuarios = usuarios.filter(first_name__icontains=nome) 
        #paginando
        paginator = Paginator(usuarios, 4)
        page = request.GET.get('page')
        usuarios_todos = paginator.get_page(page)
        contextUsu = { 
            #tres ultimos usuarios
            'usuarios_ultimos': ultimos_usu,
            #todos os usuarios
            'usuarios': usuarios_todos,
        }
        return render(request, 'usuarios/usuarios.html', contextUsu)

def deleta_usuario(request, usuario_id):
    usu = get_object_or_404(User, pk=usuario_id)
    usu.delete()
    messages.success(request, 'Usuario deletado com sucesso!')
    return redirect('usuarios')

def edita_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    context = { 'usuario_editar': usuario }
    return render(request, 'usuarios/editar-usuario.html', context)

def atualiza_usuario(request, usuario_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            usuario_id = request.POST['id']
            u = User.objects.get(pk=usuario_id)
            nome_pri = request.POST['primeiro_nome']
            nome_seg = request.POST['segundo_nome']
            email = request.POST['email']
            senha = request.POST['senha']
            senha2 = request.POST['senha2']
            nivel_usuario = request.POST['nivel_usuario']
            #validacoes
            if not campo_vazio(nome_pri):
                messages.error(request, 'O campo nome não pode ficar vazio')
                return redirect('edita_usuario', usuario_id)
            if not campo_vazio(nome_seg):
                messages.error(request, 'O campo nome não pode ficar vazio')
                return redirect('edita_usuario', usuario_id)
            if not campo_vazio(email):
                messages.error(request, 'O campo email não pode ficar vazio')
                return redirect('edita_usuario', usuario_id)
            if not campo_vazio(senha):
                messages.error(request, 'O campo senha não pode ficar vazio')
                return redirect('edita_usuario', usuario_id)        
            if senha_nao_sao_iguais(senha, senha2):
                messages.error(request, 'As senhas não são iguais')
                return redirect('edita_usuario', usuario_id)
            if senha.isdigit():
                messages.error(request, 'A senha não pode conter apenas números!')
                return redirect('edita_usuario', usuario_id)
            #imagem atrelado ao usuário
            usuario_imagem = Usuario.objects.filter(pessoa=u).get() #trazendo a imagem associada ao User
            if 'foto_usuario' in request.FILES:
                usuario_imagem.foto_perfil = request.FILES['foto_usuario']
                usuario_imagem.save()
            u.first_name = nome_pri
            u.last_name = nome_seg
            u.email = email
            u.password = senha  
            if nivel_usuario == 'Usuário':
                u.is_superuser = False
                u.is_staff = False
            if nivel_usuario == 'Staff':
                u.is_superuser = False
                u.is_staff = True
            if nivel_usuario == 'Admin':
                u.is_superuser = True
                u.is_staff = True
            u.save()
            messages.success(request, 'Usuário alterado com sucesso!')
            return redirect('usuarios')
    else:
        return render(request, 'usuarios/dashboard.html')
            
#organizando as funções que se repetem
def campo_vazio(campo):
    return campo.strip()
def senha_nao_sao_iguais(senha, senha2):
    return senha != senha2