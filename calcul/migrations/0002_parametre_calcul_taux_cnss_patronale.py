# Generated by Django 4.1 on 2024-01-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calcul", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="parametre_calcul",
            name="taux_cnss_patronale",
            field=models.FloatField(null=True),
        ),
    ]
