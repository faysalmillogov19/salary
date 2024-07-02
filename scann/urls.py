from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("cnib", views.import_cnib, name='scann_cnib'),
    path("test", views.test),
]