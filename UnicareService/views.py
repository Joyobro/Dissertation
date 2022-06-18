from django.shortcuts import render
import json
from datetime import date, timedelta,datetime

# Create your views here.
from django.http import HttpResponse, JsonResponse
from UnicareService.models import Organisation, Profile, Device,Sensordata
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from UnicareService.utils.utils import POST
from django.core import serializers
from UnicareService.health.HeartRate import HeartRate
def organisations(request):
    id = request.GET.get("id")
    if (id is None):
        return JsonResponse(list(Organisation.objects.values()), safe=False)
    else:
        organisation = Organisation.objects.filter(id=id)
        if organisation.exists():

            return JsonResponse(list(organisation.values()), safe=False)
        else:
            return JsonResponse("{'status':'failed'}", safe=False)


def profile(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        if (id is None):
            orgid = request.GET.get("orgid")
            profiles = []
            for profile in Profile.objects.filter(orgid=orgid).values():
                devicesetup = json.loads(profile["devicesetup"])
                today = date.today()
                age = (date.today() - profile["dob"]) // timedelta(days=365.2425)
                new_profile = {"profileid_id": profile["id"],
                               "firstname": profile["firstname"],
                               "lastname": profile["lastname"],
                               "name": profile["firstname"] + " " + profile["lastname"],
                               "dob": profile["dob"],
                               "orgid": profile["orgid_id"],
                               "deviceid": profile["deviceid_id"],
                               "email": profile["email"],
                               "contactno": profile["contactno"],
                               "age": age,
                               "gender": profile["gender"],
                               "address": profile["address"],
                               "postcode": profile["postcode"],
                               "famcontact": profile["famcontact"],
                               "sosno1": devicesetup["sosno1"],
                               "sosno2": devicesetup["sosno2"],
                               "sosno3": devicesetup["sosno3"],
                               "fencecenter": devicesetup["fencecenter"],
                               "fenceradiussize": devicesetup["fenceradiussize"],
                               "sosinterval": devicesetup["sosinterval"],
                               "datainterval": devicesetup["datainterval"],
                               "gpsinterval": devicesetup["gpsinterval"]}
                profiles.append(new_profile);
            result = {"data": profiles}
            return JsonResponse(result, safe=False)
        else:
            profile = Profile.objects.filter(pk=id)
            if profile.exists():
                return JsonResponse(list(profile.values()), safe=False)
            else:
                return JsonResponse("{'status':'failed'}", safe=False)
    elif request.method == 'POST':
        devicesetup = {"sosno1": request.POST["sosno1"],
                       "sosno2": request.POST["sosno2"],
                       "sosno3": request.POST["sosno3"],
                       "fencecenter": request.POST["fencecenter"],
                       "fenceradiussize": request.POST["fenceradiussize"],
                       "sosinterval": request.POST["sosinterval"],
                       "datainterval": request.POST["datainterval"],
                       "gpsinterval": request.POST["gpsinterval"]}
        organisation = Organisation.objects.filter(id=request.POST["orgid"])[0];

        profiles_ext = Profile.objects.filter(id=request.POST["profileid_id"]);
        new_deviceid = request.POST["deviceid"];
        # if a profile exists and the deviceid passed is a none/empty, it means we are dettaching a device from a profile or the profile never had a device assgined
        if (profiles_ext.exists()):
            profile = profiles_ext[0];
            if new_deviceid is None or new_deviceid=="":
                device = profile.deviceid
                if (device is not None):
                    device.status = "Available"
                    device.assignedname = None
                    device.save()

                Profile.objects.update_or_create(id=request.POST["profileid_id"],
                                                 defaults={"firstname": request.POST["firstname"],
                                                           "lastname": request.POST["lastname"],
                                                           "email": request.POST["email"],
                                                           "contactno": request.POST["contactno"],
                                                           "gender": request.POST["gender"],
                                                           "dob": request.POST["dob"],
                                                           "address": request.POST["address"],
                                                           "famcontact": request.POST["famcontact"],
                                                           "orgid": organisation,
                                                           "deviceid": None,
                                                           "postcode": request.POST["postcode"],
                                                           "devicesetup": json.dumps(devicesetup)})

                result = {'status': 'success'}
                return JsonResponse(result)

        devices = Device.objects.filter(id=new_deviceid)
        if (devices.exists()):
            device = devices[0];
            device.status = "Assigned"
            device.assignedname = request.POST["firstname"] + " " + request.POST["lastname"]
            device.save()
            Profile.objects.update_or_create(id=request.POST["profileid_id"],
                                             defaults={"firstname": request.POST["firstname"],
                                                       "lastname": request.POST["lastname"],
                                                       "email": request.POST["email"],
                                                       "contactno": request.POST["contactno"],
                                                       "gender": request.POST["gender"],
                                                       "dob": request.POST["dob"],
                                                       "address": request.POST["address"],
                                                       "famcontact": request.POST["famcontact"],
                                                       "orgid": organisation,
                                                       "deviceid": device,
                                                       "postcode": request.POST["postcode"],
                                                       "devicesetup": json.dumps(devicesetup)})
        else:
            Profile.objects.update_or_create(id=request.POST["profileid_id"],
                                             defaults={"firstname": request.POST["firstname"],
                                                       "lastname": request.POST["lastname"],
                                                       "email": request.POST["email"],
                                                       "contactno": request.POST["contactno"],
                                                       "gender": request.POST["gender"],
                                                       "dob": request.POST["dob"],
                                                       "address": request.POST["address"],
                                                       "famcontact": request.POST["famcontact"],
                                                       "orgid": organisation,
                                                       "postcode": request.POST["postcode"],
                                                       "devicesetup": json.dumps(devicesetup)})



        result = {'status': 'success'}
        return JsonResponse(result)
    elif request.method == 'DELETE':
        profiles = Profile.objects.filter(pk=id)
        if profiles.exists():
            profile = profiles[0];
            profile.delete()
            return JsonResponse("{'status':'done'}", safe=False)

def device(request):
    if request.method == "GET":
        id = request.GET.get("id")
        if (id is not None):
            device = Device.objects.filter(pk=id)
            if device.exists():
                device_binding_info = Profile.objects.filter(deviceid=id)
                profile_info = device_binding_info[0].profileid

                result = {'device_info': device.values(), 'binding_info': profile_info}

                return JsonResponse(list(result), safe=False)
        else:
            orgid = request.GET.get("orgid")
            devices = Device.objects.filter(orgid=orgid).values("id", "type", "model", "regtime", "status",
                                                                "assignedname")
            result = {"data": list(devices)}
            return JsonResponse(result, safe=False)
    elif request.method == "POST":
        id = request.POST["id"]
        type = request.POST["type"]
        status = request.POST["status"]
        regTime = request.POST["regtime"]
        model = request.POST["model"]
        orgid = request.POST["orgid"]
        organisation = Organisation.objects.filter(id=orgid)[0]
        profileid = request.POST["profileid_id"]
        profiles = Profile.objects.filter(id=profileid)
        if profiles.exists():
            profile = profiles[0]
            status = "Assigned"
        else:
            profile = None
            status = "Available"

        device = Device(id=id, type=type, status=status, regtime=regTime, model=model, orgid=organisation)
        device.save()
        result = {'status': 'success'}
        return JsonResponse(result)
    elif request.method == "DELETE":
        id = request.POST['id']
        device = Device.objects.filter(id=id)
        device.delete()
        result = {'status': 'success'}
        return JsonResponse(result)

@csrf_exempt
def notification(request):
    if request.method=="GET":
        profileid = request.GET["profileid"]
        action = request.GET["action"]
        profiles = Profile.objects.filter(id=profileid)
        if(profiles.exists):
            device = profiles[0].deviceid
            token = device.token
            result = POST(token,action)
            if(result.json()["success"]==1):
                return JsonResponse({"status":"success"}, safe=False)
            else:
                return JsonResponse({"status": "failed"}, safe=False)

@csrf_exempt
def dashboard(request):
    if request.method == 'GET':
            orgid = request.GET.get("orgid")
            profiles = []
            for profile in Profile.objects.filter(orgid=orgid).values():
                age = (date.today() - profile["dob"]) // timedelta(days=365.2425)
                sensordata = Sensordata.objects.filter(profileid=profile["id"]).order_by('-timestamp').first()
                if(sensordata is not None):
                    new_profile = {"profileid": profile["id"],
                                   "name": profile["firstname"] + " " + profile["lastname"],
                                   "dob": profile["dob"],
                                   "hr":sensordata.hr,
                                   "step":sensordata.step,
                                   "timestamp":sensordata.timestamp,
                                   "lat":sensordata.lat,
                                   "lg":sensordata.lg,
                                   "battery":sensordata.battery,
                                   "batterystatus": sensordata.batterystatus,
                                   "status":sensordata.status,
                                   "age": age,
                                   "gender": profile["gender"]}
                else:
                    new_profile = {"profileid": profile["id"],
                                   "name": profile["firstname"] + " " + profile["lastname"],
                                   "dob": profile["dob"],
                                   "hr": "No Device",
                                   "step": "No Device",
                                   "battery": "No Device",
                                   "lat": "No Device",
                                   "lg": "No Device",
                                   "batterystatus": "No Device",
                                   "age": age,
                                   "gender": profile["gender"]}
                profiles.append(new_profile);

            profiles.reverse()
            result = {"data": profiles,"status":"success"}
            return JsonResponse(result, safe=False)


@csrf_exempt
def regdevice(request):
    if(request.method=="GET"):
        id = request.GET["id"]
        token = request.GET["token"]
        Device.objects.update_or_create(id=id,
                                        defaults={"token":token})

        profiles = Profile.objects.filter(deviceid=id).values("devicesetup")
        if(profiles.exists()):
            result = profiles[0]
            return JsonResponse({"result":json.loads(result["devicesetup"])},safe=False)
        else:
            return JsonResponse({"result":"devicenotassigned"})


def gpsdata(request):
    if (request.method == "GET"):
        profileid = request.GET["profileid"]
        sensordata = Sensordata.objects.filter(profileid=profileid).exclude(lat=-1000,lg=-1000).order_by('-timestamp').first()
        result = {"lat":sensordata.lat,"lg":sensordata.lg,"timestamp":sensordata.timestamp}
        return JsonResponse({"status": "success", "data": result}, safe=False)

@csrf_exempt
def sensordata(request):
    if(request.method=="POST"):
        try:
            sensor_data_array = json.loads(request.body)
            hm = HeartRate()
            # print(sensor_data_array)
            for sensor in sensor_data_array:
                id=sensor["deviceId"]
                profiles = Profile.objects.filter(deviceid=id).values("id","devicesetup")

                if (profiles.exists()):
                    result = profiles[0]
                    if("ppgData" in sensor):
                        ppgData = sensor["ppgData"]
                        ppgBuffer = ppgData['ppgBuffer']
                        # sample_rate = int(len(ppgBuffer)/((ppgData['endTime']-ppgData['startTime'])/1000))
                        hr = int((hm.process_signal(ppgBuffer)))
                        # hr = 0

                        sensordata = Sensordata(deviceid=id, profileid=result["id"],lat=sensor["lat"], lg=sensor["log"],
                                                battery=sensor["battery"], step=sensor["step"], ppg=sensor["ppgData"], hr=hr,
                                                timestamp=sensor["timestamp"],batterystatus=sensor["batteryStatus"],status=sensor["status"],
                                                accelerometer=sensor["accBuffer"],light=sensor["lightBuffer"],stress=0.0,bloodpressure=None)
                    else:
                        sensordata = Sensordata(deviceid=id, profileid=result["id"],lat=sensor["lat"], lg=sensor["log"],
                                                battery=sensor["battery"], step=sensor["step"], ppg=None,
                                                timestamp=sensor["timestamp"],batterystatus=sensor["batteryStatus"],status=sensor["status"],
                                                accelerometer=sensor["accBuffer"],light=sensor["lightBuffer"],stress=0.0,bloodpressure=None)
                    sensordata.save()
            return JsonResponse({"result": json.loads(result["devicesetup"])}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"result": "exceptions"}, safe=False)
    elif (request.method=="GET"):
        profileid = request.GET["profileid"]
        # today = datetime.now().date()
        today = datetime.now()
        start = datetime(today.year, today.month, today.day, today.hour-8)
        sensordata = Sensordata.objects.filter(profileid=profileid,
                                               timestamp__range=(start.timestamp()*1000,datetime.now().timestamp()*1000)).order_by("timestamp").values("timestamp","hr","step","battery");
        return JsonResponse({"status":"success","data": list(sensordata)}, safe=False)


