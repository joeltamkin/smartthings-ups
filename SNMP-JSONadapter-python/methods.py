from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

def get(self, oid):
    cmdGen = cmdgen.CommandGenerator()
    #print "polling for: %s" % self.name
    
    try:
        eI, eS, eIdx, varBinds = cmdGen.getCmd (
            cmdgen.CommunityData(str(self.device.community)),
            cmdgen.UdpTransportTarget((str(self.device.ip), str(self.device.port))),
            str(oid))
        
        if eI:
           print(eI)
        else:
            if eS:
               print('%s at %s' % (eS.prettyPrint(),eI and varBinds[int(eI)-1] or '?'))
            else:
               #print "VarBinds: %s" % varBinds
               for name, val in varBinds:
                   if (name.prettyPrint() == oid):
                      return val
                    
    except Exception, ex:
        print "exception: %s" % str(ex)
        return -1

    return 0


def getnext(self, oid):
    cmdGen = cmdgen.CommandGenerator()
    #print "polling for: %s" % self.name
    
    try:
        eI, eS, eIdx, varBindTable = cmdGen.nextCmd (
            cmdgen.CommunityData(str(self.device.community)),
            cmdgen.UdpTransportTarget((str(self.device.ip), str(self.device.port))),
            str(oid))
        
        if eI:
           print(eI)
        else:
            if eS:
               print('%s at %s' % (eS.prettyPrint(),eI and varBinds[int(eI)-1] or '?'))
            else:
               #for varBinds in varBindTable:
               #    for name, val in varBinds:
               #        print('%s = %s' % (name.prettyPrint(), val))
               #print "varbindtable: %s" % varBindTable 
               return varBindTable
                    
    except Exception, ex:
        print "exception: %s" % str(ex)
        return -1

    return 0

    #return [[('1.3.6.1.2.1.33.1.6.2.1.2.27','1.3.6.1.2.1.33.1.6.3.14')],
    #        [('1.3.6.1.2.1.33.1.6.2.1.3.27','123456')]]

def lookup(self, table, value):
    return value in self.device.tables[table].values
