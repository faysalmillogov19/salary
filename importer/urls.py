from django.urls import path
from . import views

urlpatterns = [
      path('importPersonnel', views.upload_excel, name='importPersonnel'),
]