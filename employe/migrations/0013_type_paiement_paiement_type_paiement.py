# Generated by Django 4.1 on 2024-02-14 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("employe", "0012_paiement_indemnite_fonction_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Type_paiement",
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
                ("libelle", models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="paiement",
            name="type_paiement",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="employe.type_paiement",
            ),
        ),
    ]
