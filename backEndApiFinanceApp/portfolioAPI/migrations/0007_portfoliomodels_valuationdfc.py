# Generated by Django 5.0.6 on 2024-11-22 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioAPI', '0006_portfoliomodels_dy'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfoliomodels',
            name='valuationDFC',
            field=models.FloatField(blank=True, null=True),
        ),
    ]