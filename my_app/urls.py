from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('datepicker_poc', views.datepicker_poc, name='datepicker_poc'),
    path('calender_poc', views.calender_poc, name='calender_poc'),

    path('event_schedule', views.event_schedule, name='event_schedule'),

    path('render_calender', views.render_calender, name='render_calender'),
    path('fetch_events', views.fetch_events, name='fetch_events'),
    path('create_new_event', views.create_new_event, name='create_new_event'),

    path('user_profile', views.profile_detailed_view, name='user_profile'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('book_session/', views.process_booking, name='book_session'),
    path('charge/', views.payment_done, name='charge'),
]
