from device_defs import *

devicedata = [
    {
        'name':'snmp.ups1',
        'ip':'192.168.1.251',
        'snmpversion':'v1',
        'community':'LiebertEM',
        'port':'161',
        'devicedef': LIEBERT_GXT3,
        'category':'ups',
        'pollspec': {
            'alarm': 5,
            'normal': 30
            }
        }
    ]

