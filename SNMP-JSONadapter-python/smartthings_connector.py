import requests

class SmartThingsConnector:
    def __init__(self, base_url='', client_id='', client_secret='', access_token=''):
    
        #todo handle OAuth setup

        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.params = {'access_token' : access_token}

        self.jsonupdate_url = "%(base_url)s/%(client_id)s/update" % locals()

    def jsonupdate(self, update):
        """
        updates a SmartThings system vis REST call w/ JSON payload specified by update
        """
        r = requests.put(self.jsonupdate_url, data = update, params = self.params)
        return r
        
        

   
