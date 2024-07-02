from django.urls import path
from employe.views import (index, liste, ajouter_employe, update_empl_data,delete_employe, get_contrats,
    form,ajouter_contrat,liste_contrat,update_contrat_data, detail_contrat,liste_structure, update_structure, 
    delete_structure, ajouter_structure, detail_structure, liste_employe_structure, 
    ajouter_dossiers, dossier, deletedossier, update_dossier, get_employes)
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index, name='index'),
    path('personel',views.liste, name='personel'),
    path('update_empl_data/<int:id>',views.update_empl_data, name='updateemploye'),
    path('delete_employe/<int:id>',views.delete_employe, name='deleteemploye'),
    path('form',views.form, name='form'),
    path('add_employe',views.ajouter_employe, name='add_employe'),
    path('contrat',views.liste_contrat, name='contrat'),
    path('update_contrat_data/<int:id>',views.update_contrat_data, name='update_contrat'),
    path('delete_contrat/<int:id>',views.delete_contrat, name='deletecontrat'),
    path('add_contrat',views.ajouter_contrat, name='add_contrat'),
    path('detail_contrat/<int:id>',views.detail_contrat, name='detail_contrat'),
    path('structure', views.liste_structure, name= 'structure'),
    path('update_structure/<int:id>',views.update_structure, name='update_structure'),
    path('delete_structure/<int:id>',views.delete_structure, name='delete_structure'),
    path('add_stucture',views.ajouter_structure, name='add_structure'),
    path('detail_structure/<int:id>',views.detail_structure, name='detail_structure'),
    path('liste_employe_structure/<int:structure_id>/employes', views.liste_employe_structure, name='liste_employe_structure' ),
    path('get_contrats/<int:employe_id>/', views.get_contrats, name='get_contrats'),
    path('dossier/<int:id>/', views.dossier, name='dossier_employe'),
    path('add_dossiers/<int:id>/', views.ajouter_dossiers, name='add_dossiers'),
    path('update-dossiers/<int:id>/', views.update_dossier, name='update_dossiers'),
    path('delete-dossiers/<int:id>/', views.deletedossier, name='deletedossier'),
    path('upload-contrat-doc/', views.upload_contrat_doc, name='upload_contrat_doc'),
    path('contrat-pdf/<int:id>/', views.generate_contract_pdf, name='contrat_pdf'),
    path('show-employe/<int:employe_id>/', views.get_employes, name='show_employe'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)