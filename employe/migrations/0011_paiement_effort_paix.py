# Generated by Django 4.1 on 2024-01-30 00:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0010_contrat_prime_astreinte"),
    ]

    operations = [
        migrations.AddField(
            model_name="paiement",
            name="effort_paix",
            field=models.FloatField(null=True),
        ),
    ]
