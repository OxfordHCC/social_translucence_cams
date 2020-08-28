import os
from arlo_st.env import FS_ROOT
from arlo_st.db import Library, Issue

stream_end_sentinel = object()

try:
    os.mkdir(FS_ROOT)
    print("Created fs root directory")
except FileExistsError:
    print("Fs root already initialised.")
    
#Files are stored on fs as .mp4 
def getAll():
    return os.listdir(FS_ROOT)

#get file system contents
#get library entries from database
#removed = library\files
#assume no added, because we don't really care about manually added videos
#for all removed, raise Issue()

def raiseMissingEntryIssue(entry):
    issue = Issue.create(message=f"Missing video file {entry}! Someone deleted it externally.")
    issue.save()
    
def integrityCheck():
    fsEntries = set(getAll())
    dbEntries = set([video['fsname'] for video in Library.select()])
    removed = dbEntries - fsEntries
    for entry in removed:
        raiseMissingEntryIssue(entry)
    return 0

def resolve(local_id):
    return os.path.join(FS_ROOT, local_id)

def read_file(local_id=None):
    if local_id is None:
        raise FileNotFoundError()

    file_path = resolve(local_id)
    f = open(file_path, "rb")
    def gen():
        with f:
            while bytes_arr := f.read(1000):
                yield bytes_arr
    return gen()
    

#TODO: what happens if exception is raised during writing?
def write_file(local_id, file_stream):
    file_path = resolve(local_id)
    with open(file_path, 'wb') as f:
        for byte_arr in file_stream:
            f.write(byte_arr)
    return local_id

def remove_file(local_id):
    file_path = resolve(local_id)
    os.remove(file_path)
