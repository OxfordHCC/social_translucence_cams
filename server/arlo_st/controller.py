from arlo_st.db import Library, Camera, CaptureAdapter
from arlo_st import adapters

#get registered cameras from local db
def getCameras():
    return list(Camera.select().dicts())


def get_camera_stream(camera_id):
    camera = Camera.get_by_id(camera_id)
    adapter = CaptureAdapter.get_by_id(camera.adapter)
    adapter_instance = adapters.get_instance(adapter)
    return adapter_instance.get_stream_url(camera)
