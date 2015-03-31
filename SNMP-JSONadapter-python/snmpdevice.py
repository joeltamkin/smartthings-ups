import threading, Queue, json

class SNMPtable:
    def __init__(self, device, name, poll_function=None, conversion_function=None, filter_function = None, values=None):

        self.name = name
        self.values = values
        self.device = device
        
        self.__poll = poll_function[0]
        self.__pollkwargs = poll_function[1]

        if conversion_function:
            self.__convert = conversion_function
        else:
            self.__convert = lambda x: x
            
        self.__updated = True
    
    def poll(self, dev_tables):
        """
        poll() uses the polling and conversion functions specified for this table to retrieve it
        returns the table and a flag indicating whether the table has changed since the last poll
        """
        vals = self.__convert(self.__poll(self,**self.__pollkwargs))
        if (self.values != vals):
            self.values = vals
            self.__updated = True
        else:
            self.__updated = False

        return self.values, self.__updated

    
    def toJSON(self):
        """
        toJSON() returns a JSON representation of the SNMPtable, which is null until we
        find a reason to return an intermediate table on the REST interface.
        """
        return None  # could be: {'name': self.name, 'values': self.values}

    def __repr__(self):
        return "<SNMPtable {'name': self.name, 'values': self.values}>"
    
                
    def __str__(self):
        return "<SNMPtable> %(name)s: %(tabledata)s" % {'name': self.name, 'tabledata': str(map(str, self.values))}
    
class SNMPpoint:
    def __init__(self, device, name, poll_function, conversion_function=None, value=None, devstate_trigger=None):
        self.name = name
        self.value = value
        self.device = device

        self.__poll = poll_function[0]
        self.__pollkwargs = poll_function[1]

        if conversion_function:
            self.__convert = conversion_function
        else:
            self.__convert = lambda x: x
            
        self.__updated = True   

    def poll(self, dev_tables):
        """
        poll() uses the polling and conversion functions specified for this point to retrieve it
        returns the point's value and a flag indicating whether the value has changed since the last poll
        """
        val = self.__convert(self.__poll(self,**self.__pollkwargs))
        if (self.value != val):
            self.value = val

            self.__updated = True
        else:
            self.__updated = False

        return self.value, self.__updated

    def toJSON(self):
        """
        toJSON() returns a JSON representation of the SNMPpoint, including name and value
        """
        return {'name': self.name, 'value': str(self.value)}

    def __repr__(self):
        return "<SNMPpoint {'name': self.name, 'values': self.value}>"
    
                
    def __str__(self):
        return "<SNMPpoint> %(name)s: %(value)s" % {'name': self.name, 'value': str(self.value)}


class SNMPdevice:

    def __init__(self, name, ip, snmpversion, community, port, category, devicedef, pollspec, result_q, pollinterval=30):
        self.name = name
        self.ip = ip
        self.port = port
        self.snmpversion = snmpversion
        self.community = community
        self.category = category
        self.pollspec = pollspec
        self.pollpoint = None

        self.thread = SNMPdevicePollerThread(self, result_q) 

        self.tables = dotdict()
        self.points = dotdict()
        
        for table in devicedef['_tables']:
            self.tables[table['name']] = SNMPtable(device=self, **table)
        
        for point in devicedef['_points']:
            self.points[point['name']] = SNMPpoint(device=self, **point)

        if ('_pollspecpoint' in devicedef.keys()) and (type(pollspec) == dict):
            self.pollpoint = devicedef['_pollspecpoint']
            self.pollinterval = min(self.pollspec, key=self.pollspec.get)
        else:
            print "No or incomplete polling spec - using fixed polling interval: %s seconds" % pollinterval
            self.pollinterval = pollinterval

    def poll(self):
        #try:
            ret = dotdict({'name': self.name,
                   'category': self.category,
                   'points': dotdict()})
            
            for table in self.tables:
                self.tables[table].poll(self.tables)
                
            for point in self.points:
                val, updated = self.points[point].poll(self.tables)

                if updated:
                    ret.points[self.points[point].name] = str(self.points[point].value)

                    if (self.points[point].name == self.pollpoint):
                        try:
                            print "Adjusting poll interval to: %s seconds" % self.pollspec[self.points[point].value]
                            self.pollinterval = self.pollspec[self.points[point].value]
                        except KeyError:
                            print "Error: Invalid pollspec value - using minimum defined polling rate"
                            self.pollinterval = min(self.pollspec, key=self.pollspec.get)
            return ret
        #except:
            #print "polling device %s failed" % self.name
            #self.pollstate = 'fail'

    def setState(self, state, value):
        self.states[state] = value        

    def toJSON(self):
        """
        toJSON() returns a JSON-serializable of the SNMPdevice, including name and points
        """
        return {'name': self.name, 
                'category': self.category,
                #'tables': map(lambda t: self.tables[t], self.tables.keys()), # no need for this right now
                'points': map(lambda p: self.points[p], self.points.keys())}
                          
    def __repr__(self):
        return "<SNMPdevice> %(category)s/%(name)s: %(tablecount)s Tables, %(pointcount)s Points" % \
                {'category': self.category, 'name': self.name, 'tablecount': len(self.tables), 'pointcount': len(self.points)}
    
                
    def __str__(self):
        header = self.__repr__
        snmpparams = "IP: %(ip)s\nPort: %(port)s\nSNMP version: %(version)s\nCommunity: %(community)s\n" % \
                     {'ip':self.ip, 'port':self.port,'version':self.snmpversion,'community':self.community}
        snmptables = "Tables: %s\n" % (str(map(str, self.tables)))
        snmppoints = "Points: %s\n" % (str(map(str, self.points)))
        return "%s%s%s" % (snmpparams, snmptables, snmppoints)
        
class SNMPdevicePollerThread(threading.Thread):
    def __init__(self, device, result_q):
        super(SNMPdevicePollerThread, self).__init__()

        self.device = device
        self.result_q = result_q
        self.stopflag = threading.Event()

    def run(self):
        while not self.stopflag.isSet():
            try:
                result = self.device.poll()
                if result.points:
                    print "Thread %s got updates on %s: %s" % (self.name, result['name'], result['points'])

                    result_json = json.dumps(result,
                              sort_keys=True,
                              indent=4,
                              skipkeys=True)

                    self.result_q.put(result_json)

                self.stopflag.wait(self.device.pollinterval)
                    
            except Queue.Empty:
                continue
            
    def join(self, timeout=None):
        self.stopflag.set()
        super(SNMPdevicePollerThread, self).join(timeout)


class dotdict(dict):
    """utility class to provide dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__
    __repr__ = dict.__repr__
    __str__ = dict.__str__
    
