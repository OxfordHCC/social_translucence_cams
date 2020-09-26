import threading
import uuid
import requests
from arlo_st.db import Library
from arlo_st import libraryFs
from peewee import DoesNotExist

class RecordingNotFound(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return f'Recording not found: {self.message}'

# simply swaps the DoesNotExist exception with RecordingNotFound (to
# be handled by flask)
def get_library_model(video_id):
    try:
        return Library.get_by_id(video_id)
    except DoesNotExist:
        raise RecordingNotFound("recording does not exist")

def do_sync_recording(library_model, file_stream):
    local_id = str(uuid.uuid4())
    try:
        # write new file
        libraryFs.write_file(local_id, file_stream)

        # remove old file if exists
        if library_model.location_local is not None:
            libraryFs.remove_file(library_model.location_local)

        # update db model with new location
        library_model.location_local = local_id
        library_model.save()
    except Exception as e:
        # if anything goes wrong, remove_file
        libraryFs.remove_file(local_id)
        raise e
    

def sync_recording(library_model, file_stream):
    if isinstance(library_model, str):
        library_model = get_library_model(library_model)
    
    threading.Thread(
        target=do_sync_recording,
        args=(library_model, file_stream)
    ).start()

    return None

def read_recording(library_model):
    if isinstance(library_model, str):
        library_model = get_library_model(library_model)

    try:
        return libraryFs.read_file(library_model.location_local)
    except DoesNotExist:
        raise RecordingNotFound("recording does not exist")
    except FileNotFoundError:
        raise RecordingNotFound("local file not found")

def get_all():
    return list(Library.select().dicts())
