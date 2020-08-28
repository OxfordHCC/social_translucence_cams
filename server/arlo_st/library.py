import threading
import uuid
from queue import simplequeue
import requests
from peewee import doesnotexist
from arlo_st.db import library
from arlo_st import libraryFs


class RecordingNotFound(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return f'Recording not found: {self.message}'


#simply swaps the DoesNotExist exception with RecordingNotFound (for flask handling)
def get_library_model(video_id):
    try:
        return Library.get_by_id(video_id)
    except DoesNotExist:
        raise RecordingNotFound("recording does not exist")

def do_sync_recording(library_model, file_stream):
    local_id = str(uuid.uuidv4())

    #write new file
    libraryFs.write_file(local_id, file_stream)

    #remove old file
    libraryFs.remove_file(library_model.location_local)

    #update db
    library_model.location_local = local_id
    library_model.save()
        
def snyc_recording(video_id):
    library_model = get_library_model(video_id)
    
    try:
        remote_url = library_model.location_remote
        r = requests.get(remote_url, stream=True, timeout=3)
        r.raise_for_status()
        
        q = SimpleQueue()
        
        threading.Thread(
            target=do_sync_recording,
            args=(library_model, r.iter_content(chunk_size=1000), q)
        ).start()

        return None
    except requests.exceptions.HTTPError:
        raise RecordingNotFound('remote location unreachable')
    except requests.exceptions.Timeout:
        raise RecordingNotFound('remote location unreachable')


#Old sync and stream code: will delete once checked out
#def sync_recording(library_model, file_stream, q):
#    local_id = str(uuid.uuid4())
#    libraryFs.write_file(local_id, file_stream, q)

    #update library mode
#    library_model.location_local = local_id
#    library_model.save()


# def read_remote(library_model):
#     try:
#         remote_url = library_model.location_remote
#         r = requests.get(remote_url, stream=True, timeout=3)
#         r.raise_for_status()
        
#         q = SimpleQueue()
        
#         threading.Thread(
#             target=sync_recording,
#             args=(library_model, r.iter_content(chunk_size=1000), q)
#         ).start()

#         def gen():
#             while True:
#                 bytes_arr = q.get()
#                 if bytes_arr is libraryFs.stream_end_sentinel:
#                     break
#                 yield bytes_arr
#         return gen()
#     except requests.exceptions.HTTPError:
#         raise RecordingNotFound('remote location unreachable')
#     except requests.exceptions.Timeout:
#         raise RecordingNotFound('remote location unreachable')

def read_recording(video_id):
    library_model = get_library_model(video_id)
    try:
        return libraryFs.read_file(library_model.location_local)
    except DoesNotExist:
        raise RecordingNotFound("recording does not exist")
    except FileNotFoundError:
        raise RecordingNotFound("local file not found")
