

def test_fresh_db(get):
    r = get('/adapter')
    assert r.headers['Content-Type'] == 'application/json'
    assert r.json() == []

def test_post_malformed(get, post):
    r = post('/adapter')
    assert r.status_code == 400
    r = get('/adapter')
    assert r.status_code == 200
    assert r.json() == []

def test_post_invalid_type(get, post):
    r = post('/adapter', json={
        "type": "ustreamer",
        "name": "dummy adapter",
        "options":{"aaa":1}
    })
    assert r.status_code == 400
    r = get('/adapter')
    assert r.status_code == 200
    assert r.json() == []

def test_arlo_adapter(post, get):
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
    to_date = "20200101" #these don't matter for the fake client either
    arlo_library = arlo_client.GetLibrary(from_date, to_date)
    r = get('/library')
    assert len(r.json()) == len(arlo_library)
    

    
    


