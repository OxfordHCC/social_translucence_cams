
def test_empty_logs(auth_get):
    r = auth_get('/library')
    logs = r.json()['data']
    assert type(logs) == list
    assert len(logs) == 0
