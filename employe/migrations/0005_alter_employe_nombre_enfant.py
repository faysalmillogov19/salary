# Generated by Django 4.1 on 2024-01-16 16:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0004_paiement_tpa"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employe",
            name="nombre_enfant",
            field=models.IntegerField(default=0),
        ),
    ]
