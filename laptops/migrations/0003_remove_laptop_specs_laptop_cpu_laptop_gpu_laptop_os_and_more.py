# Generated by Django 5.2.1 on 2025-06-04 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptops', '0002_inventory_delete_laptopinventory_alter_brand_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laptop',
            name='specs',
        ),
        migrations.AddField(
            model_name='laptop',
            name='cpu',
            field=models.CharField(blank=True, max_length=100, verbose_name='Processador'),
        ),
        migrations.AddField(
            model_name='laptop',
            name='gpu',
            field=models.CharField(blank=True, max_length=100, verbose_name='Placa de Vídeo'),
        ),
        migrations.AddField(
            model_name='laptop',
            name='os',
            field=models.CharField(blank=True, max_length=100, verbose_name='Sistema Operacional'),
        ),
        migrations.AddField(
            model_name='laptop',
            name='other',
            field=models.TextField(blank=True, verbose_name='Outras Informações'),
        ),
        migrations.AddField(
            model_name='laptop',
            name='ram',
            field=models.CharField(blank=True, max_length=50, verbose_name='Memória RAM'),
        ),
        migrations.AddField(
            model_name='laptop',
            name='screen',
            field=models.CharField(blank=True, max_length=100, verbose_name='Tela'),
        ),
        migrations.AddField(
            model_name='laptop',
            name='storage',
            field=models.CharField(blank=True, max_length=100, verbose_name='Armazenamento'),
        ),
    ]
