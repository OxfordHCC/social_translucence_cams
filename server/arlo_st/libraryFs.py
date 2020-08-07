import os
from arlo_st.env import FS_ROOT
from arlo_st.db import Library, Issue

try:
    os.mkdir(FS_ROOT)
    print("created fs root directory")
except FileExistsError:
    print("fs root already initialised")
    
#Files are stored on fs as .mp4 
def getAll():
    return os.listdir(FS_ROOT)

#get file system contents
#get library entries from database
#removed = library\files
#assume no added, because we don't really care about manually added videos
#for all removed, raise Issue()
def integrityCheck():
    def raiseMissingEntryIssue(entry):
        issue = Issue.create(message=f"Missing video file {entry}! Someone deleted it externally.")
        issue.save()
    fsEntries = set(libraryFs.getAll())
    dbEntries = set([video['fsname'] for video in Library.select()])
    removed = dbEntries - fsEntries
    for entries in removed:
        raiseMissingEntryIssue(entry)
    return 0
