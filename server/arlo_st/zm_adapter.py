from datetime import datetime
from base64 import b64decode
import json
import requests
from arlo_st.library import RecordingNotFound
from arlo_st.db import Camera, Library

API_ROOT = "/zm/api"
LOGIN_ENDPOINT = "/host/login.json"
MONITORS_ENDPOINT = "/monitors.json"
MONITOR_ENDPOINT = lambda x: f"monitors/{x}.json"
EVENTS_ENDPOINT = "/events.json"

class TokenExpiredException(Exception):
    pass

def raise_token_expired(jwt_token):
    [header, payload, signature] = jwt_token.split('.')
    payload = json.loads(b64decode(payload + '==='))
    time_now = datetime.now()
    time_expiry = datetime.fromtimestamp(payload['exp'])
    if time_now > time_expiry:
        raise TokenExpiredException()

class ZMMonitor:
    def populate_from_api(self, api_dict):
        self.name = api_dict['Name']
        self.id = api_dict['Id']
        self.width = api_dict['Width']
        self.height = api_dict['Height']
        
        return self
        
class ZoneminderClient:
    def __init__(self, options):
        zm_host = options['zm_host']
        zm_user = options['zm_user']
        zm_pass = options['zm_pass']
        self.zm_user = zm_user
        self.zm_pass = zm_pass
        self.zm_host = zm_host
        self.token = self.get_new_token()

    # -> String
    def api_to(self,  endpoint):
        pieces = [self.zm_host, API_ROOT, endpoint]
        stripped = [s.strip('/') for s in pieces]
        return '/'.join(stripped)

    # -> {}
    def get_new_token(self):
        req_url = self.api_to(LOGIN_ENDPOINT)
        r = requests.post(req_url, data={
            "user": self.zm_user,
            "pass": self.zm_pass
        })
        res = r.json()
        return res

    # -> JWT (String)
    def get_refresh_token(self):
        token = self.token['refresh_token']
        raise_token_expired(token)
        return token

    # -> JWT (String)
    def get_access_token(self):
        token = self.token['access_token']
        raise_token_expired(token)
        return token

    # -> None
    def refresh_token(self):
        try:
            refresh_token = self.get_refresh_token()
        except TokenExpiredException:
            self.token = self.get_new_token()
            refresh_token = self.get_refresh_token()

        req_url = self.api_to(LOGIN_ENDPOINT)
        r = requests.post(req_url, data={
            "refresh_token": refresh_token
        })
        self.token = r.json()

    # -> JWT (String)
    def get_valid_access_token(self):
        try:
            token = self.get_access_token()
        except TokenExpiredException:
            self.refresh_token()
            token = self.get_access_token()
        return token

    # -> requests.Response
    def api_get(self, url):
        url = self.api_to(url)
        token = self.get_valid_access_token()
        tokenized_url = f"{url}?token={token}"
        return requests.get(tokenized_url)

    # -> requests.Response
    def api_post(self, url):
        url = self.api_to(url)
        token = self.get_valid_access_token()
        return requests.post(url, data={"access_token": token})

    # TODO: Change return type to [ZMEvent]
    # -> [{}]
    def get_events(self):
        r = self.api_get(EVENTS_ENDPOINT)
        return r.json()
    
    # -> [ZMMonitor]
    def get_monitors(self):
        r = self.api_get(MONITORS_ENDPOINT)
        monitor_dicts = r.json()['monitors']
        monitor_factory = lambda x: ZMMonitor().populate_from_api(x)
        return [
            monitor_factory(api_dict['Monitor'])
            for api_dict
            in monitor_dicts
        ]

    # @monitor_id: Number
    # -> ZMMonitor
    def get_monitor(self, monitor_id):
        r = self.api_get(MONITOR_ENDPOINT(monitor_id))
        monitor_desc = r.json()['monitor']['Monitor']
        return ZMMonitor().populate_from_api(monitor_desc)

    # @monitor_id: String
    # @mode: String | None
    # -> String
    def get_monitor_stream_url(self, monitor_id, mode='jpeg'):
        token = self.get_valid_access_token()
        monitor = self.get_monitor(monitor_id)
        url = (
            f"{self.zm_host}/zm/cgi-bin/nph-zms"
             "?scale=100"
            f"&width={monitor.width}px"
            f"&height={monitor.height}px"
            f"&mode={mode}"
             "&maxfps=30"
            f"&monitor={monitor.id}"
            f"&token={token}"
        )
        return url
    
    # @event_id: Number
    # @mode: String | None
    # -> String
    def get_event_stream_url(self, event_id, mode="mp4"):
        token = self.get_valid_access_token()
        url = (
            f"{self.zm_host}/zm/index.php"
            f"?mode={mode}"
             "&view=view_video"
            f"&eid={event_id}"
            f"&token={token}"
        )
        return url


class ZoneminderAdapter:
    def __init__(self, adapter_model):
        options = adapter_model['options']
        self.zm_client = ZoneminderClient(options)  
        self.adapter_id = adapter_model['id']

    @staticmethod
    def validate_options(options):
        assert "zm_host" in options
        assert "zm_user" in options
        assert "zm_pass" in options
    
    @staticmethod
    def get_description():
        return {
            "type": "zoneminder",
            "name": "Zoneminder",
            "options": [
                { "name": "zm_user", "type": "string", "label": "Username" },
                { "name": "zm_pass", "type": "password", "label": "Password" },
                { "name": "zm_host", "type": "string", "label": "Zoneminder Hostname"}
            ]
        }
    
    # -> iso timestamp (String)
    @staticmethod
    def convert_timestamp(remote_timestamp):
        dt = datetime.fromisoformat(remote_timestamp)
        return dt.isoformat()

    # TODO: change remote_library type to ZMEvent
    # @remote_library: {}
    # -> Library
    def to_library_model(self, remote_library):
        local = Library()
        local.id = remote_library['Event']['Id']
        local.timestamp = ZoneminderAdapter.convert_timestamp(
            remote_library['Event']['StartTime']
        )
        local.camera = remote_library['Event']['MonitorId']
        local.name = remote_library['Event']['Name']
        local.adapter = self.adapter_id
        local.removed_remote = False
        return local

    # @remote_camera: ZMMonitor
    # -> Camera
    def to_camera_model(self, remote_camera):
        local = Camera()
        local.id = remote_camera.id
        local.name = f"Camera {remote_camera.name}"
        local.adapter = self.adapter_id
        return local
    
    # -> [Camera]
    def get_remote_cameras(self):
        cameras = self.zm_client.get_monitors()
        return map(self.to_camera_model, cameras)

    # -> [Library]
    def get_remote_library(self):
        library = self.zm_client.get_events()['events']
        return map(self.to_library_model, library)
    
    # @library_model: Library
    # -> Stream/Iterator
    def get_recording_stream(self, library_model):
        try:
            url = self.zm_client.get_event_stream_url(library_model.id)
            r = requests.get(url, stream=True, timeout=3)
            r.raise_for_status()
            return r.iter_content(chunk_size=1000)
        except requests.exceptions.MissingSchema:
            raise RecordingNotFound('remote location invalid')
        except requests.exceptions.HTTPError:
            raise RecordingNotFound('remote location unreachable')
        except requests.exceptions.Timeout:
            raise RecordingNotFound('remote location unreachable')

    # @camera_model: Camera
    # -> { url: String, mime: String }
    def get_stream_url(self, camera_model):
        url = self.zm_client.get_monitor_stream_url(camera_model.id)
        return { "url": url, "mime": "jpeg" }
