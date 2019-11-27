from django.urls import path, re_path
from youtor.settings import base
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url


urlpatterns = [
    # common urls
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    url(r'^activate/(?P<user_id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('user_profile', views.user_profile_view, name='user_profile'),
    path('logout', auth_views.LogoutView.as_view(next_page=base.LOGOUT_REDIRECT_URL), name='logout'),
    path('change_password', views.change_password, name='change_password'),

    # tutor urls
    path('create_tutor_profile', views.create_tutor_profile, name='create_tutor_profile'),
    path('schedule', views.offer_scheduling, name='schedule'),
    path('create_slots', views.create_event, name='create_slot'),
    path('delete_slots', views.delete_events, name='delete_slots'),
    path('remove_subs_tags', views.remove_subs_tags, name='remove_subs_tags'),

    # student urls
    re_path('^youtor_app/tutor_search/$',views.tutor_search_result),
    re_path('^youtor_app/tutor_search_result_price/$',views.tutor_search_result_price),
    re_path('^tutor_profile/(?P<slug>[\w-]+)/$', views.tutor_detailed_view, name='tutor_detailed_view'),


    # Payment urls
    path('proceed_to_checkout', views.proceed_to_checkout, name='proceed_to_checkout'),
    path('process_tution_booking', views.process_tution_booking, name='process_tution_booking'),
    path('charge/', views.payment_done, name='charge'),
    path('payment_cancelled/', views.payment_canceled, name='payment_cancelled'),

    # ----------- booking ---------------------------
    path('booking',views.booking,name='booing'),

    # ------------ Star Rating ---------------------------
    path('rate/',views.TutorRate,name='TutorRate'),

]
