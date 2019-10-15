from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datepicker_poc', views.datepicker_poc, name='datepicker_poc'),
    path('calender_poc/<int:session_id>', views.calender_poc, name='calender_poc'),
    path('event_schedule', views.event_schedule, name='event_schedule'),
]
