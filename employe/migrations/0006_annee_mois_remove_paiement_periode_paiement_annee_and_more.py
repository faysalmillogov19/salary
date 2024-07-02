# Generated by Django 4.1 on 2024-01-17 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0005_alter_employe_nombre_enfant"),
    ]

    operations = [
        migrations.CreateModel(
            name="Annee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exercice", models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Mois",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("libelle", models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="paiement",
            name="periode",
        ),
        migrations.AddField(
            model_name="paiement",
            name="annee",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="employe.annee",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="paiement",
            name="mois",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to="employe.mois",
            ),
            preserve_default=False,
        ),
    ]
