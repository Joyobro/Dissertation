from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView
from .usermanage import userviews

urlpatterns = [
    url(r'^organisation$', views.organisations, name='organisation'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^notification$', views.notification, name='notification'),
    url(r'^gpsdata$', views.gpsdata, name='gpsdata'),
    url(r'^device$', views.device, name='device'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^device/register$', views.regdevice, name='regdevice'),
    url(r'^sensordata$', views.sensordata, name='sensordata'),
    url(r'^downloadcsv$', views.downloadcsv, name='downloadcsv'),
    url(r'^adminsignin$', userviews.adminsignin, name='adminsignin'),
    url(r'^adminsignout$', userviews.adminsignout, name='adminsignout'),

]
