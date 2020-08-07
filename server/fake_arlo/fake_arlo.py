import os
import json

class Arlo(object):
    def __init__(self, user, passwd):
        dirname = os.path.dirname(__file__)
        data_file_path = os.path.join(dirname,'fake_data.json')

        with open(data_file_path, encoding="utf-8") as f:
            self.data = json.loads(f.read())
            
    def GetLibrary(self, from_date, to_date):
        return self.data['library']
    
    def GetDevices(self, device_type):
        return self.data[device_type]

        
