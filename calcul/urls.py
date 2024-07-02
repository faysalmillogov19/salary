from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("paiement/<int:id_contrat>", views.liste_paiement, name='liste_paiement'),
    path("pointage/<int:id_paiement>", views.pointage, name='pointage'),
    path("icp/<int:id_paiement>", views.paiement_icp, name='paiement_icp'),
    path("ifc/<int:id_paiement>", views.paiement_ifc, name='paiement_ifc'),
    path("delete/<int:id_paiement>", views.delete_paiement, name='delete_paiement'),
    path("payer/<int:id_paiement>", views.payer, name='payer_paiement'),
    path("details/<int:id_paiement>", views.detail_paiement, name='detail_paiement'),
]