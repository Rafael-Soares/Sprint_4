from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    pessoa = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(verbose_name='Foto de Perfil', upload_to='imagens_usuarios/', default='imagens_usuarios/user.png', blank=True)
    def __str__(self):
        return self.pessoa.first_name