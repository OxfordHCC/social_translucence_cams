import requests

creds = {
    "username": "foo",
    "password": "bar"
}

def test_register(post):
    r = post('/register', json=creds)
    response = r.json()
    assert "access_token" in response


def test_login(post):
    r = post('/login', json=creds)
    response = r.json()
    assert "access_token" in response
    
    token = response['access_token']
    assert len(token.split('.')) == 3
    

def test_invalid_login(post):
    unreg_creds = {
        "username": "unregistered",
        "password": "foobar"
    }
    
    r = post('/login', json=unreg_creds)
    
    assert r.status_code == 401

def test_unauthorized(get):
    r = get('/library')
    assert r.status_code == 401


def test_authorized(base_url, post):
    r = post('/login', json=creds)
    response = r.json()
    token = response['access_token']

    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    r = requests.get(f'{base_url}/library', headers=headers)
    assert r.status_code == 200
