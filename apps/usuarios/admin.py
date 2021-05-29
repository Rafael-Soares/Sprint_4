from django.contrib import admin
from .models import *

class Listantando(admin.ModelAdmin):
    list_display = ('id', 'pessoa')
    list_display_links =('id', 'pessoa')
admin.site.register(Usuario, Listantando)