from arlo_st.db import Library, Camera


#get library content from local database
def getLibrary():
    return list(Library.select().dicts())

#get registered cameras from local db
def getCameras():
    return list(Camera.select().dicts())


