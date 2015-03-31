import json
import requests

from constants import STBASEURL, STAPPGUID, STAPPTOKEN, DEFAULTPOLLDELAY, DEFAULTALARMPOLLDELAY
from device_defs import *
from devices import devicedata

from snmpdevice import SNMPdevice, SNMPdevicePollerThread
from smartthings_connector import SmartThingsConnector

import threading, Queue

ST = SmartThingsConnector(
        STBASEURL,
        STAPPGUID,
        "clientsecret-notusedyet",
        STAPPTOKEN )

devices = []
devthread = []

result_q = Queue.Queue()
    
for dev in devicedata:
    #print dev
    devices.append(SNMPdevice(result_q=result_q,**dev))

for dev in devices:
    dev.thread.start()

while len(devices):
    result_json = result_q.get()
    print "thread returned %s" % result_json
    req = ST.jsonupdate(result_json)
    print "Update response-code: %s" % req.status_code
             
