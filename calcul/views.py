from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from employe.models import Contrat, Employe, Paiement, Pointage, Mois, Annee, Type_paiement
#from salary.employe.views import detail_contrat
from .models import Parametre_calcul, Parametre_ifc, Constante_calcule
from .Traitement import taux_horaire, paiement_volume_horaire, calcul_prime_anciennete, calcul_prime_quart, calcul_prime_panier, calcul_prime_quart_sftp, calcul_cnss, calcul_cnss_patronale, calcul_tpa, calcul_IUTS, calcul_ifc, calcul_icp
from django.db.models import Q, Sum,Max,Min, Avg


from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from SystemConf.Back_Control_Access import is_admin


@login_required(login_url="user_signin")
def liste_paiement(request, id_contrat):
    contrat=Contrat.objects.get(id=id_contrat)
    data=Pointage.objects.filter(paiement__contrat_id=id_contrat)
    mois=Mois.objects.all()
    annee=Annee.objects.all().last()
    par=Parametre_calcul.objects.get(id=1)
    return render(request,'calcul/paiements.html',{'data':data,'contrat':contrat,'mois':mois,'annee':annee, 'par':par})

@login_required(login_url="user_signin")
def pointage(request, id_paiement):

    if request.method=="POST":

        contrat=Contrat.objects.get(id=request.POST.get('id_contrat'))
        if id_paiement>0:
            paiement=Paiement.objects.get(id=id_paiement)
            pointage=Pointage.objects.filter(paiement_id=id_paiement).first()
        else:
            paiement=Paiement()
            paiement.type_paiement=Type_paiement.objects.get(id=1)
            pointage=Pointage()
        if request.POST.get("nb_jour_travail_normal"):
            pointage.nb_jour_travail_normal=int(request.POST.get("nb_jour_travail_normal"))
        if request.POST.get("nb_h_normal"):
            pointage.nb_h_normal=int(request.POST.get("nb_h_normal"))
        if request.POST.get("nb_h_15"):
            pointage.nb_h_15=int(request.POST.get("nb_h_15"))
        if request.POST.get("nb_h_35"):
            pointage.nb_h_35=int(request.POST.get("nb_h_35"))
        if request.POST.get("nb_h_50"):
            pointage.nb_h_50=int(request.POST.get("nb_h_50"))
        if request.POST.get("nb_h_60"):
            pointage.nb_h_60=int(request.POST.get("nb_h_60"))
        if request.POST.get("nb_h_120"):
            pointage.nb_h_120=int(request.POST.get("nb_h_120"))
        if request.POST.get("nb_jour"):
            pointage.nb_jour=int(request.POST.get("nb_jour"))
        if request.POST.get("nb_quart"):
            pointage.nb_quart=int(request.POST.get("nb_quart"))
        if request.POST.get("surplus"):
            paiement.surplus_salaire=float(request.POST.get("surplus"))
        if request.POST.get("relicat"):
            paiement.relicat_salaire=float(request.POST.get("relicat"))
            
            
        paiement.annee=Annee.objects.get(id=request.POST.get('annee'))
        paiement.mois=Mois.objects.get(id=request.POST.get('mois'))
        paiement=salaire_sur_site(contrat, paiement, pointage)
        paiement.save()
        paiement.salaire_net=round( paiement.salaire_net-paiement.effort_paix )
        paiement.save()
        pointage.paiement=paiement
        pointage.save()
        #data=Paiement.objects.filter(contrat_id=id_paiement)
        #return redirect('liste_paiement', id_contrat=contrat.id)
        
        return redirect('liste_paiement', id_contrat=contrat.id)

@login_required(login_url="user_signin")
def salaire_sur_site(contrat, paiement, pointage):
    par=Parametre_calcul.objects.get(id=1)
    taux_h=0
    sal_brute=0
    prime_ancien=0
    prime_quart=0
    prime_panier=0
    
    if contrat.prime_anciennete:
       prime_ancien=calcul_prime_anciennete(par, contrat.nombre_annee_travail, contrat.salaire_base)

    if pointage.nb_jour_travail_normal:
        contrat.salaire_base= (contrat.salaire_base * pointage.nb_jour_travail_normal) / par.nb_jour_travail_normal
    
    if contrat.mode_calcul.id==3:
        sal_brute=contrat.salaire_base + (contrat.indemnite_logement+ contrat.indemnite_fonction+ contrat.indemnite_transport + contrat.indemnite_risque) + (contrat.prime_nourriture + contrat.prime_lait + contrat.prime_salissure + contrat.augmentation_octobre_2019 + contrat.augementation_special_pourcentage+contrat.sursalaire) + prime_ancien
        print('##############')
        
        taux_h=float( taux_horaire(par, sal_brute) )
        print(f'Taux horaire: {taux_h}')
        p_v_h=paiement_volume_horaire(pointage, taux_h)
        print(f'Heures Sup: {p_v_h}')
        sal_brute=sal_brute+p_v_h
        print(f'SAL BRUTE: {sal_brute}')
        if pointage.nb_quart:
            prime_quart=round(calcul_prime_quart_sftp(par, pointage.nb_quart, sal_brute))
            print(f'Prime Quart: {prime_quart}')

    else:
        taux_h=float( taux_horaire(par, contrat.salaire_base) )
        p_v_h=contrat.salaire_base+paiement_volume_horaire(pointage, taux_h)
        sal_brute=p_v_h + (contrat.indemnite_logement+ contrat.indemnite_fonction+ contrat.indemnite_transport + contrat.indemnite_risque) + (contrat.prime_nourriture + contrat.prime_lait + contrat.prime_salissure) +  prime_ancien
        
        if pointage.nb_quart:
            prime_quart=round(calcul_prime_quart(par, pointage.nb_quart, taux_h))


    if pointage.nb_jour:
        prime_panier=round(calcul_prime_panier(par, pointage.nb_jour, taux_h))

    sal_brute=sal_brute  + (prime_quart + prime_panier)
    

    cnss=calcul_cnss(par, sal_brute)
    cnss_patronal=calcul_cnss_patronale(par, sal_brute)
    tpa=calcul_tpa(par, sal_brute)
    iuts=calcul_IUTS(par, sal_brute, contrat )

    ### SAVE PAIEMENT
    paiement.salaire_net= round( sal_brute+paiement.relicat_salaire-(iuts+cnss+paiement.surplus_salaire) )
    paiement.salaire_base=contrat.salaire_base
    paiement.prime_ancien=prime_ancien
    paiement.prime_quart=prime_quart
    paiement.prime_panier=prime_panier
    paiement.prime_nourriture=contrat.prime_nourriture
    paiement.prime_lait=contrat.prime_lait
    paiement.salaire_brut=round( sal_brute )
    paiement.indemnite_fonction=contrat.indemnite_fonction
    paiement.indemnite_logement=contrat.indemnite_logement
    paiement.indemnite_transport=contrat.indemnite_transport
    paiement.indemnite_risque=contrat.indemnite_risque
    paiement.augmentation_octobre_2019=contrat.augmentation_octobre_2019
    paiement.augementation_special_pourcentage=contrat.augementation_special_pourcentage
    paiement.sursalaire=contrat.sursalaire
    paiement.cotitsation_cnss=round( cnss )
    paiement.cnss_patronal=round( cnss_patronal )
    paiement.tpa=round( tpa )
    paiement.iuts=round( iuts )
    paiement.effort_paix=par.taux_effort_paix*paiement.salaire_net
    paiement.contrat=contrat

    return paiement


@login_required(login_url="user_signin")
def paiement_icp(request, id_paiement):
    if request.method=='POST':
        contrat=Contrat.objects.get(id=request.POST.get('id_contrat'))
        sal_brut=Paiement.objects.filter(contrat=contrat).aggregate(montant=Avg("salaire_brut", default=0))['montant']
        par=Parametre_calcul.objects.get(id=1)

        if id_paiement > 0:
            paiement=Paiement.objects.get(id=id_paiement)
            pointage=Pointage.objects.filter(paiement=paiement).first()
        else:
            paiement= Paiement()
            paiement.type_paiement=Type_paiement.objects.get(id=2)
            pointage= Pointage()

        paiement.annee=Annee.objects.get(id=request.POST.get('annee'))
        paiement.mois=Mois.objects.get(id=request.POST.get('mois'))
        paiement.salaire_brut=sal_brut
        paiement.cotitsation_cnss=calcul_cnss(par, sal_brut)
        paiement.cnss_patronal=calcul_cnss_patronale(par, sal_brut)
        paiement.tpa=calcul_tpa(par, sal_brut)
        paiement.iuts=calcul_IUTS(par, sal_brut, contrat )
        paiement.surplus_salaire=float(request.POST.get('surplus'))
        paiement.relicat_salaire=float(request.POST.get('relicat'))
        paiement.salaire_net=paiement.salaire_brut + paiement.relicat_salaire -( paiement.iuts + paiement.cotitsation_cnss + paiement.surplus_salaire)
        paiement.effort_paix=par.taux_effort_paix*paiement.salaire_net
        paiement.contrat=contrat
        paiement.save()

        pointage.paiement=paiement
        pointage.save()

    return redirect('liste_paiement', id_contrat=paiement.contrat.id)

@login_required(login_url="user_signin")
def paiement_ifc(request, id_paiement):
    if request.method=='POST':
        contrat=Contrat.objects.get(id=request.POST.get('id_contrat'))
        sal_brut=Paiement.objects.filter(contrat=contrat).aggregate(montant=Avg("salaire_brut", default=0))['montant']
        par=Parametre_calcul.objects.get(id=1)
        par_ifc=Parametre_ifc.objects.get(id=1)
        const_calcul=Constante_calcule.objects.get(id=1)

        sal_brut=( sal_brut*par_ifc.taux*float(request.POST.get('nb_jour')) ) / const_calcul.diviseur_ifc



        if id_paiement > 0:
            paiement=Paiement.objects.get(id=id_paiement)
            pointage=Pointage.objects.filter(paiement=paiement).first()
        else:
            paiement= Paiement()
            paiement.type_paiement=Type_paiement.objects.get(id=3)
            pointage= Pointage()

        paiement.annee=Annee.objects.get(id=request.POST.get('annee'))
        paiement.mois=Mois.objects.get(id=request.POST.get('mois'))
        paiement.salaire_brut=sal_brut
        paiement.cotitsation_cnss=calcul_cnss(par, sal_brut)
        paiement.cnss_patronal=calcul_cnss_patronale(par, sal_brut)
        paiement.tpa=calcul_tpa(par, sal_brut)
        paiement.iuts=calcul_IUTS(par, sal_brut, contrat )
        paiement.surplus_salaire=float(request.POST.get('surplus'))
        paiement.relicat_salaire=float(request.POST.get('relicat'))
        paiement.salaire_net=paiement.salaire_brut + paiement.relicat_salaire -( paiement.iuts + paiement.cotitsation_cnss + paiement.surplus_salaire)
        paiement.effort_paix=par.taux_effort_paix*paiement.salaire_net
        paiement.contrat=contrat
        paiement.save()

        pointage.paiement=paiement
        pointage.save()


    return redirect('liste_paiement', id_contrat=paiement.contrat.id)

@login_required(login_url="user_signin")
def detail_paiement(request, id_paiement):
    paiement=Paiement.objects.get(id=id_paiement)
    pointage=Pointage.objects.filter(paiement=paiement)
    return render(request,'calcul/details.html',{'paiement':paiement,'pointage':pointage})

@login_required(login_url="user_signin")
def payer(request, id_paiement):
    paiement=Paiement.objects.get(id=id_paiement)
    paiement.payer=True
    paiement.save()
    return redirect('liste_paiement', id_contrat=paiement.contrat.id)

@login_required(login_url="user_signin")
def delete_paiement(request, id_paiement):
    paiement=Paiement.objects.get(id=id_paiement)
    pointage=Pointage.objects.filter(paiement=paiement).delete()
    paiement.delete()
    return redirect('liste_paiement', id_contrat=paiement.contrat_id)