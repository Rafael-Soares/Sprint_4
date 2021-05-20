
from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import render, redirect
#importação para cadastrar os usuários
from django.contrib.auth.models import User
#importação para autenticacao dos usuarios e mensagens
from django.contrib import auth, messages 

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
        return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def cadastro(request):
    if request.method == 'POST':
        email = request.POST['email']
        nome = request.POST['nome']
        username = request.POST['username']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']
    #validações
        if not campo_vazio(email):
            messages.error(request, 'O campo email não pode ficar vazio')
            return redirect('cadastro')
        if not campo_vazio(nome):
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
        user = User.objects.create_user(username=username, email=email, password=senha, first_name=nome) #cadastrando usuário
        user.save()
        messages.success(request,  'Cadastro realizado com sucesso!')
        return redirect('login')
    else:   
        return render(request, 'usuarios/cadastro.html')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect('login')
       
#organizando as funções que se repetem
def campo_vazio(campo):
    return campo.strip()
def senha_nao_sao_iguais(senha, senha2):
    return senha != senha2