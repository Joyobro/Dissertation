from django.contrib import admin
from UnicareService.models import Organisation,Profile,Device,AuthUser,Sensordata

admin.site.register(Organisation)
admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(AuthUser)
# Register your models here.