import json
from playhouse.shortcuts import model_to_dict
from arlo_st.db import CaptureAdapter, Issue, Camera, Library
from arlo_st.arlo_adapter import ArloAdapter
from arlo_st.zm_adapter import ZoneminderAdapter
from arlo_st import library

# REGISTER ADAPTERS HERE!
ADAPTER_CLASSES = [
    ArloAdapter,
    ZoneminderAdapter
]

ADAPTER_CLASS_BY_TYPE = {}
for adapterClass in ADAPTER_CLASSES:
    ADAPTER_CLASS_BY_TYPE[adapterClass.get_description()['type']] = adapterClass

# maps adapter ids to adapter instances
ADAPTER_MAP = {}

class UnknownAdapterTypeError(Exception):
    def __init__(self, adapter_type):
        self.adapter_type = adapter_type

    def __str__(self):
        return f'Unknown adapter type "{self.adapter_type}"'

class MalformedAdapterOptions(Exception):
    def __str__(self):
        return f"Malformed adapter options object."
    
# @adapter: Adapter 
# -> None
def sync_library(adapter):
    remote = set(adapter.get_remote_library())
    local = set(Library.select().where(Library.adapter == adapter.adapter_id))
    remote_removed = local - remote
    remote_added = remote - local

    #create issues for every externally removed recording
    for rremoved in remote_removed:
        Issue.create(message=f"recording {rremoved.name} removed externally")

    #add all recordings created externally
    Library.bulk_create(remote_added)
    
# @adapter: Adapter
# -> None
def sync_cameras(adapter):
    remote = set(adapter.get_remote_cameras())
    local = set(Camera.select().where(Camera.adapter == adapter.adapter_id))
    remote_removed = local - remote
    remote_added = remote - local

    #create issues for every externally removed recording
    for rremoved in remote_removed:
        Issue.insert(message=f"camera {rremoved.name} removed externally")

    #add all new cameras created externally
    Camera.bulk_create(remote_added)

# @adapter: Adapter
# -> None
def sync_recordings(adapter):
    library_models = Library.select().where(Library.adapter == adapter.adapter_id)
    for library_model in library_models:
        if library_model.location_local is None:
            try:
                file_stream = adapter.get_recording_stream(library_model)
                library.sync_recording(library_model.id, file_stream)
            except library.RecordingNotFound as e:
                print(f"Error while syncing record for adapter {adapter.adapter_id}:\n", e)

# @adapters = [Adapter] | Adapter | None
# -> None
def sync(adapters=None):
    
    if adapters is None:
        adapters = ADAPTER_MAP.values()
    try:
        for adapter in adapters:
            sync_cameras(adapter)
            sync_library(adapter)
            sync_recordings(adapter)
    except Exception as e:
        print("error in sync function", e)
        raise e

# @adapter_dict: CaptureAdapterDict
# -> Adapter
def instantiate_adapter(adapter_dict):
    # [!] we use bracket notation to raise exception if key is not
    # found
    adapter_type = adapter_dict['adapter_type']

    # get the appropriate constructor for this adapter, from the
    # adapter map
    #
    # [!] we use get to suppress the keynot found exception and
    # instead throw our custom exception. We could also
    # try:except:raise it
    adapter_constructor = ADAPTER_CLASS_BY_TYPE.get(adapter_type)
    if adapter_constructor is None:
        raise UnknownAdapterTypeError(adapter_type)

    try:
        adapter_constructor.validate_options(adapter_dict['options'])
    except AssertionError:
        raise MalformedAdapterOptions()
    
    adapter = adapter_constructor(adapter_dict)
    return adapter

# @adapter_type: String
# @name: String
# @adapter_options: Dict
# -> None
def register(adapter_type, name, adapter_options):
    adapter_constructor = ADAPTER_CLASS_BY_TYPE.get(adapter_type)
    if adapter_constructor is None:
        raise UnknownAdapterTypeError(adapter_type)

    adapter_model = CaptureAdapter.create(
        adapter_type=adapter_type,
        name=name,
        options=json.dumps(adapter_options)
    )

    adapter_dict = model_to_dict(adapter_model)
    adapter_dict['options'] = json.loads(adapter_dict['options'])
    adapter_instance = instantiate_adapter(adapter_dict)

    ADAPTER_MAP[adapter_model.id] = adapter_instance
    sync([adapter_instance])

# @adapter: CaptureAdapter.dict
# -> None
def unregister(adapter_dict):
    CaptureAdapter.get_by_id(adapter_dict['id']).delete()

# @return [CaptureAdapter.dict]
def get_registered():
    def parse_options(adapter_dict):
        adapter_dict['options'] = json.loads(adapter_dict['options'])
        return adapter_dict

    adapter_dicts = CaptureAdapter.select().dicts()
    return [ parse_options(adapter_dict) for adapter_dict in adapter_dicts ]

# @adapter: CaptureAdapter | CaptureAdapter.dict | String | None
# -> Adapter
def get_instance(adapter=None):
    if adapter is None:
        return ADAPTER_MAP.values()
    
    if type(adapter) is CaptureAdapter:
        adapter = adapter.id

    if type(adapter) is dict:
        adapter = adapter['id']
        
    return ADAPTER_MAP[adapter]

# -> [AdapterDescription]
def get_types():
    return [adapterClass.get_description() for adapterClass in ADAPTER_CLASSES]

# create adapter instances and store references in ADAPTER_MAP
# -> None
def init_adapters():
    adapter_models = get_registered()
    for adapter_model in adapter_models:
        try:
            adapter_instance = instantiate_adapter(adapter_model)
            ADAPTER_MAP[adapter_model['id']] = adapter_instance
        except:
            unregister(adapter_model)
