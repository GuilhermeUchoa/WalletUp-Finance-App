# Generated by Django 5.0.6 on 2024-06-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioAPI', '0003_portfoliomodels_porcentagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliomodels',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
