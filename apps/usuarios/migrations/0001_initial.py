# Generated by Django 3.2.3 on 2021-05-26 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario_imagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto_usuario', models.FileField(upload_to='imagens_produtos/', verbose_name='Foto do produto')),
            ],
        ),
    ]
