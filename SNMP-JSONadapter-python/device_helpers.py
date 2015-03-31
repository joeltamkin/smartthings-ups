"""
Helper functions for snmp data
"""

def RFC1628_alarmtable(x):
    if len(x):
        return map(lambda y: str(y[1]), x[0])
    else:
        return []

def RFC1628_alarmspresent(x):
    return {
              0 : "normal",
              1 : "alarm",
            }[int(x)]

def RFC1628_outputsource(x):
    return {
              1 : "other",
              2 : "none",
              3 : "normal",
              4 : "bypass",
              5 : "battery",
              6 : "booster",
              7 : "reducer"
            }[int(x)]

def RFC1628_inputlinesbad(x):
    return {
              0 : "normal",
              1 : "fail",
              2 : "fail",
              3 : "fail"
            }[int(x)]

def RFC1628_transientalarm(x):
    return {
              '': "normal",
              1 : "alarm"
            }[int(x)]
