# Generated by Django 5.0.6 on 2024-06-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os_project', '0002_remove_ordemservico_fotos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='descricao_final',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='os_fotos/'),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='km_chegada',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='km_saida',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]