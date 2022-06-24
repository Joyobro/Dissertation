from django.conf.urls import url
from django.views.generic.base import TemplateView
from . import  views

urlpatterns = [
    url(r'^admin$', views.dashboard,name='admin'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^admin/login/',views.organisations_admin,name='adminlogin'),
    url(r'^admin/',views.organisations_admin,name='adminlogin'),
    url(r'^login/', views.organisations, name='carelogin'),
    url(r'^profiles/', views.profiles, name='profiles'),
    url(r'^devices/', views.devices, name='devices'),

]