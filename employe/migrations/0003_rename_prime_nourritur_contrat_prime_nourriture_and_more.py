# Generated by Django 4.1 on 2024-01-16 13:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0002_contrat_indemnite_risque"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contrat",
            old_name="prime_nourritur",
            new_name="prime_nourriture",
        ),
        migrations.RenameField(
            model_name="contrat",
            old_name="prime_silissure",
            new_name="prime_salissure",
        ),
    ]