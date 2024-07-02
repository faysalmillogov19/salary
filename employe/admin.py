from django.contrib import admin
from .models import Employe, Contrat, SituationMatrimoniale, Diplome, Structure,TypeContrat,Specialite, Categorie

# Reg, ister your models here.

class AdminEmploye(admin.ModelAdmin):
	list_display = ('id','nom', 'prenoms', 'date_naissance')

class AdminContrat(admin.ModelAdmin):
	list_display=('id','type_contrat', 'structure')
admin.site.register(Employe, AdminEmploye)
admin.site.register(Contrat, AdminContrat)
admin.site.register(SituationMatrimoniale)
admin.site.register(Diplome)
admin.site.register(Categorie)
admin.site.register(Specialite)
admin.site.register(TypeContrat)
admin.site.register(Structure)
