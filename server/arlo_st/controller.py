from arlo_st.db import Library, Camera
from arlo_st.library import get_video


#get library content from local database
def getLibrary(videoId = None):
    if(videoId is None):
        return list(Library.select().dicts())
    return get_video(videoId)

#get registered cameras from local db
def getCameras():
    return list(Camera.select().dicts())



