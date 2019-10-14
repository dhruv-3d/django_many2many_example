from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datepicker_poc', views.datepicker_poc, name='datepicker_poc'),
]
