# Generated by Django 4.1 on 2024-01-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0003_rename_prime_nourritur_contrat_prime_nourriture_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paiement",
            name="tpa",
            field=models.FloatField(null=True),
        ),
    ]
