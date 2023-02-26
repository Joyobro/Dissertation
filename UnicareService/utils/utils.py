import requests
import json
fcmkey = "key=AIzaSyAo0ZqymBIUH2YU9NfF1pISWCVTLLMnhks"
fcmserver = "https://fcm.googleapis.com/fcm/send"


def POST(token,action,alarmid):
    headers = {'content-type': 'application/json',
               'authorization':fcmkey}
    msg = {"to": token,
           "data":
               {
                   "action": action,
                   "alarmid":alarmid
               },
           "priority": 10
           }

    return requests.post(fcmserver,data=json.dumps(msg),headers=headers)
