from django.shortcuts import render
import pandas as pd
import numpy as np
from employe.models import Employe, Contrat, Specialite, SituationMatrimoniale, Diplome, Categorie, Specialite, Structure, TypeContrat, ModeCalcule
from datetime import datetime

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from SystemConf.Back_Control_Access import is_admin


@login_required(login_url="user_signin")
# Create your views here.
def upload_excel(request):
    if request.method == 'POST':
        file = request.FILES['fichier']
        data=False
        if file.name.endswith('.xls') or file.name.endswith('.xlsx'):
            data=insert_file(file)
            #  sauvegarder dans la base de données
        return render(request,'Importer/list.html', {'data':data})
        
    return render(request, 'Importer/form.html')

@login_required(login_url="user_signin")
def insert_file(fichier):
    data=pd.read_excel(fichier)
    data = data.replace(np.nan, None)
    list=[]
    i=1
    if i==1:
        for i,row in data.iterrows():
            
            employe=Employe()
            contrat=Contrat()

            if  row['nom']:
                    employe.nom=str(row['nom'])
            
            if  row['prenom']:
                    employe.prenoms=str(row['prenom'])

            if  row['matricule']:
                    employe.numero_matricule=str(row['matricule'])

            if  row['date_naissance']:
                    #date=datetime.strptime(row['date_naissance'], "%d/%M/%Y").strftime("%Y-%m-%d")
                    date=row['date_naissance'].strftime("%Y-%m-%d")
                    employe.date_naissance=date
            
            if  row['nombre_enfant']:
                    employe.nombre_enfant=str(row['nombre_enfant'])

            if  row['specialite']:
                    specialite=Specialite.objects.filter(specialite=str(row['specialite'])).first()
                    if specialite is None:
                           specialite=Specialite()
                           specialite.specialite=str(row['specialite'])
                           specialite.save()
                    employe.specialite=specialite

            if  row['lieu_naissance']:
                    employe.lieu_naissance=str(row['lieu_naissance'])

            if  row['sexe']:
                    employe.sexe=str(row['sexe'])

            if  row['situation_matrimonial']:
                    situation=SituationMatrimoniale.objects.filter(situation_matrimoniale=row['situation_matrimonial']).first()
                    if situation is None:
                           situation=SituationMatrimoniale.objects.filter(situation_matrimonial='Célibataire').first()
                    employe.situation_matrimoniale=situation

            if  row['email']:
                    employe.email=str(row['email'])


            if  row['adresse']:
                    employe.adresse=str(row['adresse'])

            if  row['dernier_diplome']:
                    diplome=Diplome.objects.filter(diplome=str(row['dernier_diplome'])).first()
                    if diplome is None:
                           diplome=Diplome()
                           diplome.diplome=str(row['dernier_diplome'])
                           diplome.save()
                    employe.dernier_diplome= diplome

            if  row['categorie']:
                    categorie=Categorie.objects.filter(categorie=str(row['categorie'])).first()
                    if categorie is None:
                           categorie=Categorie()
                           categorie.categorie=str(row['categorie'])
                           categorie.save()
                    employe.categorie=categorie

            if  row['option']:
                    employe.option=str(row['option'])

            if  row['numero_cnss']:
                    employe.numero_cnss=str(row['numero_cnss'])

            employe.save()
            list.append(employe)
            #print(employe.prenoms)

            contrat.employe=employe

            if  row['structure']:
                    structure = Structure.objects.filter(denomination=str(row['structure'])).first()
                    if structure is None:
                           structure=Structure()
                           structure.denomination=str(row['structure'])
                           structure.save()
                    contrat.structure=structure

            if  row['description_poste']:
                    contrat.description_poste=str(row['description_poste'])

            if  row['description_profil']:
                   contrat.description_profil=str(row['description_profil'])

            if  row['lieu_affectation']:
                    contrat.lieu_affectation=str(row['lieu_affectation'])

            if  row['diplome_requis']:
                    diplome=Diplome.objects.filter(diplome=str(row['diplome_requis'])).first()
                    if diplome is None:
                           diplome=Diplome()
                           diplome.diplome=str(row['diplome_requis'])
                           diplome.save()
                    contrat.diplome_requis=diplome
            if  row['type_contrat']:
                    type=TypeContrat.objects.filter(type_contrat=str(row['type_contrat'])).first()
                    print(type.libelle)
                    contrat.type_contrat=type

            if  row['cadre']:
                    contrat.cadre=bool(str(row['cadre']))

            if  row['mode_calcul']:
                    mode=ModeCalcule.objects.get( id=int(row['mode_calcul']) )
                    if mode is None:
                           mode=ModeCalcule.objects.get( id=1 )
                    contrat.mode_calcul=mode

            if  row['date_debut']:
                    contrat.date_debut=row['date_debut'].strftime("%Y-%m-%d")

            if  row['date_fin']:
                    contrat.date_fin=row['date_fin'].strftime("%Y-%m-%d")

            if  row['salaire_base']:
                    contrat.salaire_base=str(row['salaire_base'])

            if  row['indemnite_logement']:
                    contrat.indemnite_logement=str(row['indemnite_logement'])

            if  row['indemnite_transport']:
                    contrat.indemnite_transport=str(row['indemnite_transport'])
            if  row['indemnite_fonction']:
                    contrat.indemnite_fonction=str(row['indemnite_fonction'])

            if  row['indemnite_risque']:
                    contrat.indemnite_risque=str(row['indemnite_risque'])

            if  row['prime_nourriture']:
                    contrat.prime_nourriture=str(row['prime_nourriture'])

            if  row['prime_lait']:
                    contrat.prime_lait=str(row['prime_lait'])

            if  row['prime_salissure']:
                    contrat.prime_salissure=str(row['prime_salissure'])
            if  row['prime_astreinte']:
                    contrat.prime_astreinte=str(row['prime_astreinte'])
            if  row['nombre_annee_travail']:
                    contrat.nombre_annee_travail=str(row['nombre_annee_travail'])
            if  row['prime_anciennete']:
                    contrat.prime_anciennete=bool(row['prime_anciennete'])
            if  row['prime_quart']:
                    contrat.prime_quart=bool(row['prime_quart'])
            if  row['prime_panier']:
                    contrat.prime_panier=bool(row['prime_panier'])
            
            contrat.save()

        return list

        #except:
                #return False       

