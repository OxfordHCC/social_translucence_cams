import pytest

def test_meta_fake_arlo(arlo_client):
    from_date = "19700101"
    to_date = "20200101" #these don't matter for the fake arlo client
    arlo_library = arlo_client.GetLibrary(from_date, to_date)
    assert len(arlo_library) > 0

def test_arlo_adapter(post, get, fake_arlo_server):
    jsonAdapter = {
        "adapter_type": "arlo",
        "name": "arlo adapter",
        "options":{
            "username":"foo",  #these don't actually matter for the fake arlo client
            "password":"bar"
        }
    }
    r = post('/adapter', json=jsonAdapter)
    assert r.status_code == 200, r.text

    r = get('/adapter')
    assert r.status_code == 200, r.text
    newAdapter = r.json()[0]
    del newAdapter['id']
    assert newAdapter == jsonAdapter
    
def test_arlo_cameras_synced(get, arlo_client):
    arlo_cams = arlo_client.GetDevices('camera')
    r = get('/camera')
    assert len(r.json()) == len(arlo_cams)

def test_arlo_library_synced(get, arlo_client):
    from_date = "19700101"
    to_date = "20200101" #these don't matter for the fake arlo client
    arlo_library = arlo_client.GetLibrary(from_date, to_date)
    r = get('/library')
    assert len(r.json()) == len(arlo_library)

def test_arlo_library_contents(get, arlo_client):
    from_date = "19700101"
    to_date = "20200101" #these don't matter for the fake arlo client
    arlo_library = arlo_client.GetLibrary(from_date, to_date)
    
    r = get('/library')
    server_library = r.json()

    arlo_library = sorted(arlo_library, key = lambda x: x['name'])
    server_library = sorted(server_library, key = lambda x: x['id'])

    for server_entry, arlo_entry in zip(server_library, arlo_library):
        assert server_entry['id'] == arlo_entry['name']
        assert server_entry['name'] == arlo_entry['name']
        assert server_entry['camera'] == arlo_entry['deviceId']
        assert server_entry['location_remote'] == arlo_entry['presignedContentUrl']

def test_library(get):
   r = get('/library/test')
   assert r.status_code == 200
   assert r.headers['content-type'] == 'video/mp4'

def test_library_not_found(get):
    r = get('/library/not_in_library')
    assert r.status_code == 404

def test_library_remote_not_exist(get):
    r = get('/library/video_remote_not_exist')
    assert r.status_code == 404

def test_library_remote_unreachable(get):
    r = get('/library/unreachable_remote_host')
    assert r.status_code == 404

    
    

