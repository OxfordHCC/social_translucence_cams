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

def test_adapter_types(get, post):
    r = get('/adapter-types')
    assert r.json() == [{
        "name": "Arlo",
        "type": "arlo",
        "options": {
            "username": { "type": "string", "name":"Username" },
            "password": { "type": "string", "name":"Password" }
        }
    }]

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

    

    
    


