from django.db import models

class Parametre_calcul(models.Model):
    p_taux_horaire=models.FloatField(null=True)
    min_prime_aciennete=models.FloatField(null=True)
    taux_cnss=models.FloatField(null=True)
    taux_cnss_patronale=models.FloatField(null=True)
    tpa=models.FloatField(null=True)
    taux_prime_aciennete=models.FloatField(null=True)
    taux_augmentation_prime=models.FloatField(null=True)
    taux_effort_paix=models.FloatField(null=True)
    p_prime_quart=models.FloatField(null=True)
    p_prime_quart_sftp=models.FloatField(null=True)
    p_prime_panier=models.FloatField(null=True)
    controle_cnss_taux_sal_brute=models.FloatField(null=True)
    controle_cnss_taux_sal_base=models.FloatField(null=True)
    controle_plafond_logement=models.FloatField(null=True)
    controle_plafond_transport=models.FloatField(null=True)
    controle_plafond_fonction=models.FloatField(null=True)
    controle_plafond_risque=models.FloatField(null=True)
    controle_plafond_panier=models.FloatField(null=True)
    max_controle_plafond_logement=models.FloatField(null=True)
    max_controle_plafond_transport=models.FloatField(null=True)
    max_controle_plafond_risque=models.FloatField(null=True)
    max_controle_plafond_panier=models.FloatField(null=True)
    max_controle_plafond_fonction=models.FloatField(null=True)
    taux_abatement_iuts_cadre=models.FloatField(null=True)
    taux_abatement_iuts_non_cadre=models.FloatField(null=True)
    nb_jour_travail_normal=models.IntegerField(null=True)

class Tranche_revenu(models.Model):
    min=models.FloatField(null=True)
    max=models.FloatField(null=True)
    taux=models.FloatField(null=True)

class Tranche_charge(models.Model):
    nombre=models.FloatField(null=True)
    taux=models.FloatField(null=True)

class Constante_calcule(models.Model):
    diviseur_ifc=models.FloatField(default=0)

class Parametre_ifc(models.Model):
    taux=models.FloatField(default=0)