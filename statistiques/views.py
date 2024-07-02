from turtle import update
from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
from employe.models import Structure, Employe, Contrat, Employe, Paiement
from django.db.models import Count, Sum


def stat_employe_structure(request):
	nb_employe_structure=Contrat.objects.values('structure__denomination').order_by('structure__denomination').annotate(count=Count('structure__denomination'))
	contrats=Contrat.objects.all()
	data=[]
	for c in contrats:
		k=[c.id,c.structure.denomination]
		data.append(k)
	df=pd.DataFrame(data, columns=['nombre','structure'])
	plt.figure()
	df.groupby('structure').count().plot(kind='bar')
	file_name='test'
	plt.title("Repartition des employés par structure")
	plt.savefig(file_name)
	file_url='stats/'+'graphic.png'
	shutil.move("test.png", "static/"+file_url)

	return render(request,'stats/stat_structure_employe.html',{'file_url':file_url, 'nb_employe_structure':nb_employe_structure})

def stat_paiement_structure(request):
	paiements=Paiement.objects.values('contrat__structure__denomination').order_by('contrat__structure__denomination').annotate(salaire_brut=Sum('salaire_brut'))
	print(paiements)
	data=[]
	for c in paiements:
		k=[c['salaire_brut'], c['contrat__structure__denomination']]
		data.append(k)
	df=pd.DataFrame(data, columns=['Salaire brut','structure'])
	plt.figure()
	df.groupby('structure').sum().plot(kind='bar')
	plt.xlabel('Salaire brut')
	plt.ylabel('Structure')
	plt.xticks(rotation = 0)
		
	#fig, ax = plt.subplots()
	#ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
	file_name='test'
	plt.title("Masse salariale par Structure")
	plt.savefig(file_name)
	file_url='stats/'+'graphic2.png'
	shutil.move("test.png", "static/"+file_url)

	return render(request,'stats/stat_paiement_structure.html',{'file_url':file_url, 'paiements':paiements})

def stat_paiement_employe(request):
	if request.method=='POST':
		num_mat=request.POST.get('matricule')
		debut=request.POST.get('debut')
		fin=request.POST.get('fin')
		employe=Employe.objects.filter(numero_matricule=num_mat).first()
		paiements=Paiement.objects.filter(contrat__employe__numero_matricule=num_mat)
		if debut and fin:
			paiements=paiements.filter(updated_at__gte=debut, updated_at__lte=fin)
		data=paiements.values_list('salaire_brut', 'salaire_net', 'updated_at')
		df=pd.DataFrame(data, columns=['salaire_brut', 'salaire_net', 'updated_at'])
		plt.figure()
		plt.xlabel('Dates')
		plt.ylabel('Montant')
		#plt.rcParams['figure.figsize'] = (5, 4)
		#plt.rcParams['font.size'] = '20'
		plt.xticks(rotation = 45)
		plt.plot(df.updated_at, df.salaire_brut, label='Salaire Brut' )#.dt.strftime('%d-%m-%y')
		plt.plot(df.updated_at, df.salaire_net, label='Salaire Net' )
		file_name='test'
		plt.title("Masse salariale par Structure")
		plt.legend(prop = {'size': 8})
		plt.savefig(file_name)
		file_url='stats/'+'graphic3.png'
		shutil.move("test.png", "static/"+file_url)		
		return render(request,'stats/stat_paiement_employe.html',{'file_url':file_url, 'paiements':paiements,'employe':employe,'num_mat':num_mat, 'debut':debut, 'fin':fin})
