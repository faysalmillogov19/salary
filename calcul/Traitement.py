
#################################################################################
#################################################################################
######################      Parametres figés ####################################
#################################################################################
#################################################################################
'''
par.p_taux_horaire=173.33
par.min_prime_aciennete=3
par.taux_cnss=0.055
par.taux_prime_aciennete=0.05
par.taux_augmentation_prime=0.01
par.p_prime_quart=12
par.p_prime_panier=3
par.controle_cnss_taux_sal_brute=0.08
par.controle_cnss_taux_sal_base=0.05
par.controle_plafond_logement=0.2
par.controle_plafond_transport=0.05
par.controle_plafond_fonction=0.05
par.max_par.controle_plafond_logement=75000
par.max_par.controle_plafond_transport=30000
par.max_par.controle_plafond_fonction=50000
## Si cadre 
par.taux_abatement_iuts=0.25
'''
from .models import Tranche_charge, Tranche_revenu
from employe.models import Paiement
from django.db.models import Q, Sum,Max,Min, Avg
import math
from decimal import Decimal
import decimal
from math import floor

def salaire_brut(contrat, par):
    prime_ancien=0
    prime_quart=0
    prime_panier=0

    if contrat.prime_anciennete:
       prime_ancien=calcul_prime_anciennete(par, contrat.nombre_annee_travail, contrat.salaire_base)
    
    return contrat.salaire_base + (contrat.indemnite_logement+ contrat.indemnite_fonction+ contrat.indemnite_transport + contrat.indemnite_risque) + (contrat.prime_nourriture + contrat.prime_lait + contrat.prime_salissure + contrat.prime_astreinte) + (prime_ancien + prime_quart + prime_panier)

def taux_horaire(par, sal_base):
    val=sal_base/par.p_taux_horaire
    return round(val)

def paiement_volume_horaire(pointage, taux_horaire):
    montant=0
    dict=[ 
            #{'majoration':0, 'nombre_heure':float(pointage.nb_h_normal)},
            {'majoration':0.15, 'nombre_heure':float(pointage.nb_h_15)},
            {'majoration':0.35, 'nombre_heure':float(pointage.nb_h_35)},
            {'majoration':0.5, 'nombre_heure':float(pointage.nb_h_50)},
            {'majoration':0.6, 'nombre_heure':float(pointage.nb_h_60)},
            {'majoration':1.2, 'nombre_heure':float(pointage.nb_h_120)},
    ]
    for p in dict:
        val= taux_horaire*(1+p['majoration'])*p['nombre_heure']
        montant+=val
    return montant

def calcul_prime_anciennete(par, nb_annee, sal_base):
    prime=0
    surplus=(nb_annee-par.min_prime_aciennete)
    if surplus>=0:
        pourcentage=(par.taux_augmentation_prime*surplus) + par.taux_prime_aciennete
        prime=pourcentage*sal_base
    return prime

def calcul_prime_quart(par, nb_quart, t_horaire):
    return par.p_prime_quart*float(nb_quart)*t_horaire

def calcul_prime_quart_sftp(par, nb_quart, sal_brute):
    return sal_brute * par.p_prime_quart_sftp*float(nb_quart)

def calcul_prime_panier(par, nb_jour, t_horaire):
    val= float(t_horaire) / float(par.p_prime_panier)
    return val*float(nb_jour)

def calcul_cnss(par, sal_brute):
    return sal_brute * par.taux_cnss

def calcul_cnss_patronale(par, sal_brute):
    return sal_brute * par.taux_cnss_patronale

def calcul_tpa(par, sal_brute):
    return sal_brute * par.tpa


def tranche_applicable(contrat, base_imposable):
    
    base_imposable = math.floor(base_imposable)
    
    max=Tranche_revenu.objects.all().aggregate(Max('min'))
    min=Tranche_revenu.objects.all().aggregate(Min('min'))
    plafond=0
    montant=0

    if base_imposable > max['min__max']:
        plafond=max['min__max']
        montant= (base_imposable - max['min__max']) * Tranche_revenu.objects.filter(min=max['min__max']).first().taux
    else:
        tranche=Tranche_revenu.objects.filter(min__lte=base_imposable, max__gte=base_imposable).first()
        plafond= tranche.min
        montant=(base_imposable-tranche.min)*tranche.taux
    
    tranches=Tranche_revenu.objects.filter(min__lt=plafond ,max__lte=plafond )
    for tr in tranches:
            mt=(tr.max-tr.min)*tr.taux
            montant= montant + mt

    return montant


def abattement_charge(contrat):
    nb_charge=contrat.employe.nombre_enfant
    marie=contrat.employe.situation_matrimoniale.id
    sexe=contrat.employe.sexe
    if sexe=="M" and marie==1:
        nb_charge+=1
    
    max_charge=Tranche_charge.objects.all().aggregate(Max('nombre'))
    if nb_charge >= max_charge['nombre__max'] :
        return Tranche_charge.objects.filter(nombre=max_charge['nombre__max']).first().taux
    else :
        return Tranche_charge.objects.filter(nombre=nb_charge).first().taux
    

    
def calcul_IUTS(par, sal_brute, contrat ):
    controle_cnss=min(contrat.salaire_base*par.controle_cnss_taux_sal_base, sal_brute*par.controle_cnss_taux_sal_brute)
    base_imposable=sal_brute-controle_cnss
    
    ### controle plafond
    controle_logement=min(base_imposable*par.controle_plafond_logement, contrat.indemnite_logement ,par.max_controle_plafond_logement)
    controle_transport=min(base_imposable*par.controle_plafond_transport, contrat.indemnite_transport, par.max_controle_plafond_transport)
    controle_fonction=min(base_imposable*par.controle_plafond_fonction, contrat.indemnite_fonction,par.max_controle_plafond_fonction)
    #controle_risque=min(base_imposable*par.controle_plafond_risque, contrat.indemnite_risque,par.max_controle_plafond_risque)
    #controle_panier=min(base_imposable*par.controle_plafond_panier, contrat.prime_panier,par.max_controle_plafond_panier)
    
    ### Abattement IUTS
    taux_abatement_iuts=par.taux_abatement_iuts_non_cadre
    if contrat.cadre:
        taux_abatement_iuts=par.taux_abatement_iuts_cadre
    abattement_iuts= taux_abatement_iuts * contrat.salaire_base


    ### Nouvelle base imposable
    base_imposable-=(controle_logement+controle_transport+controle_fonction)+abattement_iuts
    base_imposable=floor(base_imposable/100)*100
    base_imposable=round(int(base_imposable), -2)
    
    if base_imposable<=0:
        return 0
    
    ## IUTS Brut
    iuts_brut=tranche_applicable(contrat, base_imposable)
    ## Abattement Charge familiale
    abat_charge=iuts_brut*abattement_charge(contrat)
    ##IUTS NET
    iuts_net=iuts_brut-abat_charge
    
    return iuts_net
    
def calcul_ifc(par, contrat):
    sal_brut=Paiement.objects.filter(contrat=contrat).aggregate(sal_brut=Avg("salaire_brut")) 


def calcul_icp(par, contrat):
    sal_brut=Paiement.objects.filter(contrat=contrat).aggregate(montant=Avg("salaire_brut")) 
    return sal_brut.montant
##########################################################################
##########################################################################
##########################################################################
##############################        TEST   #############################
##########################################################################
##########################################################################
'''
taux_h=taux_horaire(par , sal_base)
p_v_h=paiement_volume_horaire(pointages, taux_h)
prime_ancien=calcul_prime_anciennete(nb_annee, par.min_prime_aciennete, par.taux_prime_aciennete, par.taux_augmentation_prime, sal_base)
prime_quart=calcul_prime_quart(par.p_prime_quart, nb_quart, taux_h)
prime_panier=calcul_prime_panier(par.p_prime_panier, nb_jour, taux_h)
salaire_brute=p_v_h + (indem_logement+ indem_fonction+ indem_transport + indem_risque) + (prime_nourriture + prime_lait + prime_salissure) + (prime_ancien + prime_quart + prime_panier)
cnss=calcul_cnss(salaire_brute, par.taux_cnss)
iuts=calcul_IUTS(salaire_brute, sal_base, indem_logement, indem_fonction, indem_transport )
#print(taux_h)
#print(p_v_h)
#print(prime_ancien)
#print(prime_quart)
#print(prime_panier)
#print(salaire_brute)
#print(cnss)
print(iuts)
'''