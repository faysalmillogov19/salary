from django.db import models

class Taxe(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.libelle} - {self.description}"

    class Meta:
        db_table = "taxe_table"


class JourFerier(models.Model):
    libelle = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.libelle} ({self.date}) - {self.description}"

    class Meta:
        db_table = "jour_ferier"


class TarifHeureSup(models.Model):
    taux = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    jourFerie = models.BooleanField(default=False)
    nuit=models.BooleanField(default=False)
   
    def __str__(self):
        return f"Taux : {self.taux}"

    class Meta:
        db_table = "tarif_heure_sup"


class Nuit(models.Model):
    est_nuit = models.BooleanField()
    min = models.IntegerField()

    def __str__(self):
        return f"Est nuit : {self.est_nuit} - Minimum : {self.min}"

    class Meta:
        db_table = "nuit_table"

"""
class ElementSalaire(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.libelle} - {self.description}"

    class Meta:
        db_table = "element_salaire"
"""
