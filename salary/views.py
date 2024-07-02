# from django.shortcuts import render, redirect

# def index(request):
#     return render(request, 'index.html')

# def list(request):
#     personel=[
#         {'id':1,'matricule':'0022301', 'nom':'OUEDRAOGO', 'prenom':'Hamado','date_naiss':'14/12/1989','lieu_naiss':'Mogtedoo'},
#         {'id':2,'matricule':'0022302', 'nom':'YAMEOGO', 'prenom':'Stephane Cedric','date_naiss':'02/04/1997','lieu_naiss':'Ouagadougou'},
#         {'id':3,'matricule':'0022303', 'nom':'TRAORE', 'prenom':'Saydou','date_naiss':'04/02/1990','lieu_naiss':'Abidjan RCI'},
#         {'id':4,'matricule':'0022304', 'nom':'KONE', 'prenom':'Bakary','date_naiss':'12/06/1999','lieu_naiss':'Bobo Dioulasso'},
#         {'id':5,'matricule':'0022305', 'nom':'Zongo', 'prenom':'Jean Isidore','date_naiss':'12/11/1995','lieu_naiss':'Koudougou'},
#     ]
#     return render(request,'list.html',{'personel':personel})

# def form(request):
#     return render(request,'Formulaire.html')