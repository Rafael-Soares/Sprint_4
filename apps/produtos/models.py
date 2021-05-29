from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

CATEGORIAS = [
        ("Eletrônicos", "Eletrônicos"),
        ("Televisão", "Televisão"),
        ("Computador", "Computador"),
        ("Celular", "Celular"),
        ("Áudio e Vídeo", "Áudio e Vídeo"),
    ]

class Produto(models.Model):
    pessoa = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_produto = models.CharField('Nome do produto', max_length=200, blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, null=False, default='Eletrônicos')
    imagem_produto = models.ImageField('Foto do produto', upload_to='imagens_produtos/',default='imagens_produtos/default_image.png')
    data_criacao = models.DateTimeField('Data de criação', auto_now_add=datetime.now)
    data_modificacao = models.DateTimeField('Data de modificação', auto_now=datetime.now)
    descricao = models.TextField('Descrição', blank=True)
    preco_produto = models.FloatField('Preço do produto',max_length=10, blank=True)
    email = models.EmailField('Email',null=False)
    codigo = models.CharField('Código do produto', max_length=6, unique=True)
    slug = models.SlugField('URL de Pesquisa:', max_length=255, unique=True)
    def __str__(self):
        return self.nome_produto