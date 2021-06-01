from apps.produtos.views import atualizar_produto
from os import name
from django.contrib import admin
from django.urls import path
from . import views
#importação para redefinição de senha
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('deleta_usuario/<int:usuario_id>', views.deleta_usuario, name='deleta_usuario'),
    path('edita_usuario/<int:usuario_id>', views.edita_usuario, name='edita_usuario'),
    path('atualiza_usuario/<int:usuario_id>', views.atualiza_usuario, name='atualiza_usuario' ),
    
    #paths de redefinição de senha
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="redefinicao_senha/auth-forgot-password.html"), name="reset_password" ),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="redefinicao_senha/sucesso.html"),
    name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="redefinicao_senha/auth-redeem-password.html"),
    name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="redefinicao_senha/sucessosenha.html"),
    name="password_reset_complete" ),
]