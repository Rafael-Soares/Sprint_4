from os import name
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('meus_produtos', views.meus_produtos, name='meus_produtos'), 
    path('registrar_produtos', views.registrar_produtos, name='registrar_produtos'),
    path('deletar_produto/<int:produtinhos_id>', views.deletar_produto, name='deletar_produto'),
    path('editar_produto/<int:produtinhos_id>', views.editar_produto, name='editar_produto'),
    path('atualizar_produto/<int:produtinhos_id>', views.atualizar_produto, name="atualizar_produto"),
]