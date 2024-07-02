from django.contrib import admin
from django.urls import path
from parametre import views
from . import views



urlpatterns = [
    path('listTaxe',views.indexTaxe, name='listTaxe'),
    path("update_createTaxe/<int:id>",views.update_createTaxe,name='update_createTaxe'),
    path("destroyTaxe/<int:id>",views.destroyTaxe,name='destroyTaxe'),

    path('listjourFerie',views.indexJourFerie, name='listjourFerie'),
    path("update_createJourFerier/<int:id>",views.update_createJourFerier,name='update_createJourFerier'),
    path("destroyJourFerie/<int:id>",views.destroyJourFerier,name='destroyJourFerier'),

    path('listTarifHeureSup',views.indexTarifHeureSup, name='listTarifHeureSup'),
    path("update_createTarifHeureSup/<int:id>",views.update_createTarifHeureSup,name='update_createTarifHeureSup'),
    path("destroyTarifHeureSup/<int:id>",views.destroyTarifHeureSup,name='destroyTarifHeureSup'),

    path('listNuit',views.indexNuit, name='listNuit'),
    path("update_createNuit/<int:id>",views.update_createNuit,name='update_createNuit'),
    path("destroyNuit/<int:id>",views.destroyNuit,name='destroyNuit'),


]
