# Generated by Django 4.1 on 2024-01-29 17:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calcul", "0004_tranche_charge_tranche_revenu"),
    ]

    operations = [
        migrations.AddField(
            model_name="parametre_calcul",
            name="controle_plafond_panier",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="parametre_calcul",
            name="controle_plafond_risque",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="parametre_calcul",
            name="max_controle_plafond_panier",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="parametre_calcul",
            name="max_controle_plafond_risque",
            field=models.FloatField(null=True),
        ),
    ]
