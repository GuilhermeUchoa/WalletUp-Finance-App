# Generated by Django 5.0.6 on 2024-12-06 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioAPI', '0003_alter_portfoliomodels_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliomodels',
            name='ativo',
            field=models.CharField(max_length=250),
        ),
    ]
