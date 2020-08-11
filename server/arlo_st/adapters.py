from arlo_st.db import CaptureAdapter, Issue, Camera, Library
from arlo_st.arloLib import ArloAdapter
from playhouse.shortcuts import model_to_dict, dict_to_model
from functools import reduce
import sys
import json

#new adapters need to be registered here
ADAPTER_CLASSES = [ ArloAdapter ]

ADAPTER_CLASS_BY_TYPE = {}
for adapterClass in ADAPTER_CLASSES:
    ADAPTER_CLASS_BY_TYPE[adapterClass.getDescription()['type']] = adapterClass

#maps adapter ids to adapter instances
ADAPTER_MAP = {}

logger = None

def setLogger(toLogger):
    global logger
    logger = toLogger

class UnknownAdapterTypeError(Exception):
    def __init__(self, adapter_type):
        self.adapter_type = adapter_type
    def __str__(self):
        return f'Unknown adapter type "{self.adapter_type}"'

def getAdapter(adapter):
     return ADAPTER_MAP[adapter['id']]

def syncLibrary(adapter):
    remote = set(adapter.getRemoteLibrary())
    local = set(Library.select().where(Library.adapter == adapter.adapter_id))
    remote_removed = local - remote
    remote_added = remote - local
    for rremoved in remote_removed:
        Issue.create(message = f"Video {rremoved.name} removed externally")
    remote_added_dicts = [model_to_dict(model, recurse=False) for model in remote_added]
    Library.insert_many(remote_added_dicts).execute()

#NOTE: I'M LEAVING THE SYNC FUNCTIONS SEPARATE INTENTIONALLY. MIGHT REFACTOR LATER.
def syncCameras(adapter):
    remote = set(adapter.getRemoteCameras())
    local = set(Camera.select().where(Camera.adapter == adapter.adapter_id))
    remote_removed = local - remote
    remote_added = remote - local
    for rremoved in remote_removed:
        Issue.insert(message = f"camera {rremoved.name} removed externally")
    
    #convert back to dict array, since that is what insert_many works with
    #todo: just avoid converting to Model in the first place... let's work
    remote_added_dicts = [model_to_dict(model, recurse=False) for model in remote_added]
    Camera.insert_many(remote_added_dicts).execute()

def instantiateAdapter(adapter_dict):
    adapter_type = adapter_dict.get('adapter_type')
    adapter_constructor = ADAPTER_CLASS_BY_TYPE.get(adapter_type)
    if(adapter_constructor == None):
        raise UnknownAdapterTypeError(adapter_type)
    adapter = adapter_constructor(adapter_dict)
    return adapter

def syncAdapter(adapter):
    syncCameras(adapter)
    syncLibrary(adapter)

def add(adapter_type, name, adapter_options):
    adapter_constructor = ADAPTER_CLASS_BY_TYPE.get(adapter_type)
    if(adapter_constructor == None):
        raise UnknownAdapterTypeError(adapter_type)

    adapter_model = CaptureAdapter.create(
        adapter_type = adapter_type,
        name = name,
        options = json.dumps(adapter_options)
    )
     
    adapter_dict = model_to_dict(adapter_model)
    adapter_dict['options'] = json.loads(adapter_dict['options'])
    adapter = instantiateAdapter(adapter_dict)

    ADAPTER_MAP[adapter_model.id] = adapter
    syncAdapter(adapter)  

def get():
    #I wonder if I can move this somewhere in the CaptureAdapter model
    #This needs to be called everytime we retrieve a model from the db
    #Perhaps we can use peewee's model_to_dict with some options
    def parseOptions(adapter_dict):
        try:
            adapter_dict['options'] = json.loads(adapter_dict['options'])
        except KeyError:
            pass
        return adapter_dict

    return [ parseOptions(model) for model in CaptureAdapter.select().dicts() ]

def getTypes():
    return [adapterClass.getDescription() for adapterClass in ADAPTER_CLASSES]

def sync():
    for key, adapter in ADAPTER_MAP:
        syncAdapter(adapter)


#create adapter objects and store references in ADAPTER_MAP
#adapters are long-lived objects with state of their own
def initAdapters():
    for adapter_model in get():
         ADAPTER_MAP[adapter_model['id']] = instantiateAdapter(adapter_model)
