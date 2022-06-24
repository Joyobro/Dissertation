from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from UnicareService.models import  Organisation, AuthUser

def organisations_admin(request):
    orgs = Organisation.objects.all().values("id","name")
    context = {'orgs':orgs}
    return render(request,'page_login.html',context)

def organisations(request):
    orgs = Organisation.objects.all().values("id","name")
    context = {'orgs':orgs}
    return render(request,'page_login_alt.html',context)

def profiles(request):
    username = request.user.username
    auth_user = AuthUser.objects.filter(username=username)
    organisation = auth_user[0].orgid
    context = {'orgid': organisation.id, 'orgname': organisation.name}
    return render(request,'profiles.html',context)

def dashboard(request):
    username = request.user.username
    auth_user = AuthUser.objects.filter(username=username)
    organisation = auth_user[0].orgid
    context = {'orgid': organisation.id, 'orgname': organisation.name}
    return render(request,'dashboard.html',context)

def devices(request):
    username = request.user.username
    auth_user = AuthUser.objects.filter(username=username)
    organisation = auth_user[0].orgid
    context = {'orgid': organisation.id,'orgname':organisation.name}
    return render(request,'devices.html',context)

def admin(request):
    if(request.user.is_authenticated):
        return render(request,'dashboard.html')
    else:
        return HttpResponseRedirect(reverse('portal:adminlogin'))