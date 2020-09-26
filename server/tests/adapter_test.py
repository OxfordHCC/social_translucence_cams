def test_fresh_db(auth_get):
    r = auth_get('/adapter')
    assert r.headers['Content-Type'] == 'application/json'
    assert r.json() == {"data":[]}

def test_post_malformed(auth_get, auth_post):
    r = auth_post('/adapter')
    assert r.status_code == 400
    r = auth_get('/adapter')
    assert r.status_code == 200
    assert r.json() == {"data":[]}

def test_post_invalid_type(auth_get, auth_post):
    r = auth_post('/adapter', json={
        "type": "ustreamer",
        "name": "dummy adapter",
        "options":{"aaa":1}
    })
    assert r.status_code == 400
    r = auth_get('/adapter')
    assert r.status_code == 200
    assert r.json() == {"data":[]}

def test_post_invalid_options(auth_get, auth_post):
    r = auth_post('/adapter', json={
        "name": "test",
        "adapter_type": "zoneminder",
        "options": {
            "0":"admin",
            "1":"foobar",
            "2":""
        }
    })
    assert r.status_code == 400

def test_post_gibberish(auth_post):
    r = auth_post('/adapter', json={"gibberish":"Data"})
    assert r.status_code == 400
