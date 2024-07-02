from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("structure", views.stat_employe_structure, name='stat_employe_structure'),
    path("paiement_structure", views.stat_paiement_structure, name='stat_paiement_structure'),
    path("stat_paiement_employe", views.stat_paiement_employe, name='stat_paiement_employe'),
]