# Generated by Django 4.1 on 2024-03-26 16:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0022_contrat_poste"),
    ]

    operations = [
        migrations.AddField(
            model_name="contrat",
            name="augementation_special_pourcentage",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contrat",
            name="augmentation_octobre_2019",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contrat",
            name="sursalaire",
            field=models.BooleanField(default=False),
        ),
    ]