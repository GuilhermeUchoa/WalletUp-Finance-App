# Generated by Django 5.0.6 on 2024-07-03 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliomodels',
            name='quantidade',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]