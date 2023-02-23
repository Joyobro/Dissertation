import csv
import json
from datetime import date, timedelta,datetime
from random import randint
# Create your views here.
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from UnicareService.models import Organisation, Profile, Device,Sensordata,Alarm
from django.views.decorators.csrf import csrf_exempt
from UnicareService.utils.utils import POST
from UnicareService.health.HeartRate import HeartRate
# from UnicareService.health.HREstimator import HREstimator
# from UnicareService.health.SleepAnalizer import SleepAnalizer
import numpy as np

import traceback
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
                alarms = list(Alarm.objects.filter(profileid=profile["id"],solved=0).values())
                # today = datetime.now()
                # start = today - timedelta(days=1)
                # start = start.replace(hour=12, minute=0)
                #
                # sleeping_data = list(Sensordata.objects.filter(profileid=profile["id"],
                #                                        timestamp__range=(start.timestamp()*1000,today.timestamp()*1000),sleeping=True).order_by("timestamp").values("timestamp"))
                # sleep_start  = "n/a"
                # sleep_end = "n/a"
                # sleep_duration = "n/a"
                # if (len(sleeping_data)>0):
                #     sleep_start = sleeping_data[0]["timestamp"]
                #     sleep_end =  sleeping_data[-1]["timestamp"]
                #     total_slp_duration = int(sleeping_data[-1]["timestamp"]/1000.0-sleeping_data[0]["timestamp"]/1000.0)/60 #(in mins)
                #     sleep_duration = str(int(total_slp_duration//60))+'h '+str(int(total_slp_duration%60))+'m',
                if "deviceid_id" in profile:
                    device = profile["deviceid_id"]
                else:
                    device = None
                if(sensordata is not None):
                    new_profile = {"profileid": profile["id"],
                                   "deviceid": device,
                                   "name": profile["firstname"] + " " + profile["lastname"],
                                   "dob": profile["dob"],
                                   "hr":sensordata.hr,
                                   "spo2":sensordata.spo2,
                                   "step":sensordata.step,
                                   "timestamp":sensordata.timestamp,
                                   "lat":sensordata.lat,
                                   "lg":sensordata.lg,
                                   "battery":sensordata.battery,
                                   "batterystatus": sensordata.batterystatus,
                                   "status":sensordata.status,
                                   # "sleepstart":sleep_start,
                                   # "sleepend":sleep_end,
                                   # "sleepduration":sleep_duration,
                                   "age": age,
                                   "gender": profile["gender"],
                                   "alarms":alarms}
                else:
                    new_profile = {"profileid": profile["id"],
                                   "deviceid": device,
                                   "name": profile["firstname"] + " " + profile["lastname"],
                                   "dob": profile["dob"],
                                   "hr": "n/a",
                                   "step": "n/a",
                                   "battery": "n/a",
                                   "lat": "n/a",
                                   "lg": "n/a",
                                   "batterystatus": "n/a",
                                   "age": age,
                                   "gender": profile["gender"],
                                   "alarms":alarms}
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
            # hm = HREstimator(sample_rate=400)
            for sensor in sensor_data_array:
                id=sensor["deviceId"]
                profiles = Profile.objects.filter(deviceid=id).values("id","devicesetup")
                if (profiles.exists()):
                    result = profiles[0]
                    # spo2 = randint(90,100)
                    ppgData = sensor["ppgData"]
                    # ppgData = ppgData[ppgData!=0]
                    if(len(ppgData)>0):
                        hr = 0
                        rr = 0
                        for ppg in ppgData:
                            ppgBuffer = ppg["ppgBuffer"]
                            hr = hr+hm.process_signal(ppgBuffer)
                            rr = rr+hm.process_rr_signal(ppgBuffer)
                        hr = int(hr/len(ppgData))
                        rr = int(rr/len(ppgData))
                        # ppgBuffer = ppgData['ppgBuffer']
                        # hm.sig = ppgBuffer
                        # sample_rate = int(len(ppgBuffer)/((ppgData['endTime']-ppgData['startTime'])/1000))
                        # hr = int((hm.process_signal(ppgBuffer)))
                        # hr =0# np.mean(ppgData[-3:])#hm.calculate_heart_rate(ppgBuffer, polyorder=6, mode='nearest', smt_order=6, window_size=650, filter_order=3, cutoffs=[0.85, 3.5])
                        sensordata = Sensordata(deviceid=id, profileid=result["id"],lat=sensor["lat"], lg=sensor["log"],
                                                battery=sensor["battery"], step=sensor["step"], ppg=sensor["ppgData"], hr=hr,
                                                timestamp=sensor["timestamp"],batterystatus=sensor["batteryStatus"],status=sensor["status"],
                                                accelerometer=sensor["accBuffer"],light=sensor["lightBuffer"],gyoscope=sensor["gyoBuffer"],stress=0.0,bloodpressure=None,spo2=rr,sleeping=False,processed=False)
                    else:
                        sensordata = Sensordata(deviceid=id, profileid=result["id"],lat=sensor["lat"], lg=sensor["log"],
                                                battery=sensor["battery"], step=sensor["step"], ppg=None,
                                                timestamp=sensor["timestamp"],batterystatus=sensor["batteryStatus"],status=sensor["status"],
                                                accelerometer=sensor["accBuffer"],light=sensor["lightBuffer"],gyoscope=sensor["gyoBuffer"],stress=0.0,bloodpressure=None,spo2=None,sleeping=False,processed=False)
                    sensordata.save()

                    #alarmtype==0 /notworn
                    # if(sensor['status']=='notworn' and sensor["batteryStatus"]==0):
                    #     alarm = Alarm(deviceid=id,profileid=result["id"],timestamp=sensor["timestamp"],solved=False,alarmtype=0)
                    #     alarm.save()
                    # elif (sensor['status']=='worn' or sensor["batteryStatus"]==1):
                    #     Alarm.objects.filter(profileid=result["id"],solved=0,alarmtype=0).update(solved=True,actiontime=sensor["timestamp"],responsetime=sensor["timestamp"])

                    # profile_conf = result["devicesetup"]
                    # profile_conf = json.loads(profile_conf)
                    # today = datetime.now()
                    # start = today - timedelta(hours = 24)#datetime(today.year, today.month, today.day, today.hour-8)
                    # sensordata = Sensordata.objects.filter(profileid=result["id"],
                    #                                        timestamp__range=(start.timestamp()*1000,today.timestamp()*1000),processed=False).order_by("timestamp").values("timestamp","status","accelerometer");

                    # sensordata = list(sensordata)
                    # data_interval = int(profile_conf["datainterval"])
                    # if(len(sensordata)>=int(60/data_interval)*2): #not having enough data (2 hours here)
                    #     sleep_blocks = SleepAnalizer(data_interval).process_signal(sensordata)
                    #     Sensordata.objects.filter(profileid=result["id"],
                    #                               timestamp__range=(start.timestamp()*1000,today.timestamp()*1000),processed=False).update(processed=True)
                    #
                    #     for sleep_block in sleep_blocks:
                    #         # print("from:",datetime.fromtimestamp(sleep_block[0]/1000.0).strftime("%H:%M"))
                    #         # print("to:",datetime.fromtimestamp(sleep_block[1]/1000.0).strftime("%H:%M"))
                    #         Sensordata.objects.filter(profileid=result["id"],timestamp__range=(sleep_block[0],sleep_block[1])).update(sleeping=True)
                    #
                    #     Sensordata.objects.filter(profileid=result["id"], timestamp__range=(start.timestamp()*1000,today.timestamp()*1000),processed=False).update(processed=True)
            return JsonResponse({"result": json.loads(result["devicesetup"])}, safe=False)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"result": "exceptions"}, safe=False)
    elif (request.method=="GET"):
        profileid = request.GET["profileid"]
        # today = datetime.now().date()
        today = datetime.now()
        start = today - timedelta(hours = 24)#datetime(today.year, today.month, today.day, today.hour-8)
        sensordata = Sensordata.objects.filter(profileid=profileid,
                                               timestamp__range=(start.timestamp()*1000,today.timestamp()*1000)).order_by("timestamp").values("timestamp","hr","step","battery","spo2");
        return JsonResponse({"status":"success","data": list(sensordata)}, safe=False)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

@csrf_exempt
def downloadcsv(request):
    if(request.method=="GET"):
        try:
            profileid = request.GET["profileid"]
            profiles = Profile.objects.filter(id=profileid)
            if(profiles.exists):
                today = datetime.now()
                start = today - timedelta(hours = 24)#datetime(today.year, today.month, today.day, today.hour-8)
                filename = start.strftime("%Y-%m-%d-%H:%M")+"_"+today.strftime("%Y-%m-%d-%H:%M")
                print(filename)
                sensordata = Sensordata.objects.filter(profileid=profileid,
                                                       timestamp__range=(start.timestamp()*1000,today.timestamp()*1000)).order_by("timestamp").values("timestamp","hr","step","battery","spo2","status","accelerometer","ppg","light","gyoscope");
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename='+filename+".csv"
                writer = csv.writer(response)
                writer.writerow (["timestamp","hr","step","battery","spo2","status","accelerometer","ppg","light","gyoscope"])
                for e in sensordata.values_list("timestamp","hr","step","battery","spo2","status","accelerometer","ppg","light","gyoscope"):
                    writer.writerow(e)
                return response
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"result": "exceptions"}, safe=False)
