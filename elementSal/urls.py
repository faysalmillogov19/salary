from django.contrib import admin
from django.urls import path
from elementSal import views
from . import views



urlpatterns = [
    path('',views.index, name='listElementsalaire'),

    path("update_create/<int:id>",views.update_create,name='update_createElementSalaire'),
   # path("edit/<int:id>",views.edit,name='edit'),
   # path("update/<int:id>",views.update,name='update'),
    path("destroy/<int:id>",views.destroy,name='destroyElementSalaire'),

]
