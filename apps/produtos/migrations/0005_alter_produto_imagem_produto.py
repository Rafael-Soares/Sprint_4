# Generated by Django 3.2.3 on 2021-05-26 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0004_alter_produto_imagem_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem_produto',
            field=models.ImageField(default='imagens_produtos/default_image.png', upload_to='imagens_produtos/', verbose_name='Foto do produto'),
        ),
    ]