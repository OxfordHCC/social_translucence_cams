from arlo_st.env import Arlo #this may be terrible, go to env.py for more info
from datetime import datetime
from arlo_st.db import Camera, Library
import sys
import json

#TODO: adapter['options'] should be parsed before reaching the constructor

class ArloAdapter:
    def __init__(self, adapter_model):
        options = json.loads(adapter_model['options'])
        arlo_user = options['username']
        arlo_pass = options['password']
        self.adapter_id = adapter_model['id']
        self.arlo_client = Arlo(arlo_user, arlo_pass)
        self.basestation = self.arlo_client.GetDevices('basestation')
                    
    def toLibraryModel(self, remote_library):
        local = Library()
        local.id = remote_library['name']
        local.name = remote_library['name']
        local.camera = remote_library['deviceId']
        local.remote_location = remote_library['presignedContentUrl']
        local.adapter = self.adapter_id
        local.remote_removed = False
        return local

    def toCameraModel(self, camera):
        local = Camera()
        local.id = camera['uniqueId']
        local.name = camera['uniqueId']
        local.adapter = self.adapter_id
        return local
    
    def getRemoteLibrary(self):
        from_date = datetime.fromtimestamp(0).strftime("%Y%m%d")
        to_date = datetime.now().strftime("%Y%m%d")
        print("AAA", file=sys.stderr)
        print(from_date, file=sys.stderr)
        print(to_date, file=sys.stderr)
        remote_library = self.arlo_client.GetLibrary(from_date, to_date)
        print(remote_library, file=sys.stderr)
        return map(self.toLibraryModel, remote_library)

    # get cameras from all basestations
    def getRemoteCameras(self):
        return map(self.toCameraModel, self.arlo_client.GetDevices('camera'))
