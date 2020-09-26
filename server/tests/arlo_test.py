import pytest

#should successfully register arlo adapter
def test_register(auth_post, auth_get, fake_arlo_server):
    jsonAdapter = {
        "adapter_type": "arlo",
        "name": "arlo adapter",
        "options":{
            "username": "foo",  #these don't actually matter for the fake arlo client
            "password": "bar"
        }
    }
    r = auth_post('/adapter', json=jsonAdapter)
    assert r.status_code == 200, r.text

    r = auth_get('/adapter')
    assert r.status_code == 200, r.text
    data = r.json()['data']
    newAdapter = data[0]
    del newAdapter['id']
    assert newAdapter == jsonAdapter

#camera metadata should sync
def test_arlo_cameras_synced(auth_get, arlo_client):
    arlo_cams = arlo_client.GetDevices('camera')
    r = auth_get('/camera')
    data = r.json()['data']
    assert len(data) == len(arlo_cams)

#library meta_data should sync
def test_arlo_library_synced(auth_get, arlo_client):
    from_date = "19700101"
    to_date = "20200101" #these don't matter for the fake arlo client
    arlo_library = arlo_client.GetLibrary(from_date, to_date)
    r = auth_get('/library')
    data = r.json()['data']
    assert len(data) == len(arlo_library)

#library meta_data should be correct
def test_arlo_library_contents(auth_get, arlo_client):
    from_date = "19700101"
    to_date = "20200101" #these don't matter for the fake arlo client
    arlo_library = arlo_client.GetLibrary(from_date, to_date)
    
    r = auth_get('/library')
    server_library = r.json()['data']

    arlo_library = sorted(arlo_library, key = lambda x: x['name'])
    server_library = sorted(server_library, key = lambda x: x['id'])

    for server_entry, arlo_entry in zip(server_library, arlo_library):
        assert server_entry['id'] == arlo_entry['name']
        assert server_entry['name'] == arlo_entry['name']
        assert server_entry['camera'] == arlo_entry['deviceId']
        assert server_entry['location_remote'] == arlo_entry['presignedContentUrl']

#should be able to get recording
def test_library(auth_get):
    r = auth_get('/library/test')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'video/mp4'

#should return 404 when non-existing recording is requested
def test_library_not_found(auth_get):
    r = auth_get('/library/not_in_library')
    assert r.status_code == 404

#should return 404 when recording meta-data exists but remote location returns error
def test_library_remote_not_exist(auth_get):
    r = auth_get('/library/video_remote_not_exist')
    assert r.status_code == 404

#should return 404 when recording meta-data exists but remote location is unreachable (time-out)
def test_library_remote_unreachable(auth_get):
    r = auth_get('/library/unreachable_remote_host')
    assert r.status_code == 404

    
    

