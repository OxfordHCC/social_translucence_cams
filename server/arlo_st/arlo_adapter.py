from datetime import datetime
import requests
from arlo_st.env import Arlo ## this may be terrible, see env.py for more info
from arlo_st.db import Camera, Library
from arlo_st.library import RecordingNotFound

# TODO: adapter['options'] should be parsed before reaching the constructor

class ArloAdapter:
    def __init__(self, adapter_model):
        options = adapter_model['options']
        arlo_user = options['username']
        arlo_pass = options['password']
        self.adapter_id = adapter_model['id']
        self.arlo_client = Arlo(arlo_user, arlo_pass)
        self.basestation = self.arlo_client.GetDevices('basestation')

    @staticmethod
    def validate_options(options):
        assert "username" in options
        assert "password" in options
        
    @staticmethod
    def get_description():
        return {
            "type": "arlo",
            "name": "Arlo",
            "options": [
                { "name": "username", "type": "string", "label": "Username" },
                { "name": "password", "type": "password", "label": "Password" }
            ]
        }

    @staticmethod
    def get_timestamp(remote_library):
        remote_time = int(remote_library['utcCreatedDate'])/1000
        dt = datetime.utcfromtimestamp(remote_time)
        return dt.isoformat()

    def to_library_model(self, remote_library):
        local = Library()
        local.id = remote_library['name']
        local.name = remote_library['name']
        local.timestamp = ArloAdapter.get_timestamp(remote_library)
        local.camera = remote_library['deviceId']
        local.location_remote = remote_library['presignedContentUrl']
        local.adapter = self.adapter_id
        local.removed_remote = False
        return local

    def to_camera_model(self, camera):
        local = Camera()
        local.id = camera['uniqueId']
        local.name = f"Camera {camera['uniqueId']}"
        local.adapter = self.adapter_id
        return local

    def get_remote_library(self):
        from_date = datetime.fromtimestamp(0).strftime("%Y%m%d")
        to_date = datetime.now().strftime("%Y%m%d")
        remote_library = self.arlo_client.GetLibrary(from_date, to_date)
        return map(self.to_library_model, remote_library)

    def get_recording_stream(self, library_model):
        try:
            remote_url = library_model.location_remote
            r = requests.get(remote_url, stream=True, timeout=3)
            r.raise_for_status()
            return r.iter_content(chunk_size=1000)
        except requests.exceptions.MissingSchema:
            raise RecordingNotFound('remote location null')
        except requests.exceptions.HTTPError:
            raise RecordingNotFound('remote location unreachable')
        except requests.exceptions.Timeout:
            raise RecordingNotFound('remote location unreachable')

    # get cameras from all basestations
    def get_remote_cameras(self):
        return map(self.to_camera_model, self.arlo_client.GetDevices('camera'))
