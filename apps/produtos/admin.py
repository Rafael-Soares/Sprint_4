from django.contrib import admin
from .models import *

class ListandoProdutos(admin.ModelAdmin):
    list_display = ('id', 'pessoa', 'nome_produto')
    list_display_links = ('id','pessoa', 'nome_produto')
    list_per_page = 3
    list_filter = ('categoria',)
    search_fields = ('nome_produto',)
admin.site.register(Produto, ListandoProdutos)