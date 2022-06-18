from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.core import serializers
from UnicareService.models import AuthUser
from django.contrib.auth import authenticate,login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages


def adminsignin(request):
     username= request.POST["username"]
     pwd = request.POST["password"]
     orgid = request.POST["organisation"]
     auth_user = AuthUser.objects.filter(username=username).values()
     user = authenticate(username=username, password=pwd)

     if user is not None and user.is_active and auth_user[0].get("orgid_id")==orgid:
        login(request, user)
        return HttpResponseRedirect(reverse('portal:admin'))
     else:
         messages.error(request, 'Please check the above information')
         return HttpResponseRedirect(reverse('portal:adminlogin'))


def adminsignout(request):
    logout(request);
    return HttpResponseRedirect(reverse('portal:adminlogin'))



