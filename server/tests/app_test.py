def test_get_endpoints(auth_get):
    endpoints = [
        '/adapter',
        '/adapter/',
        '/library/',
        '/library',
        '/camera',
        '/camera/',
        '/adapter-types',
        '/adapter-types/',
        '/login',
        '/register'
    ]

    reqs = [auth_get(endpoint) for endpoint in endpoints]
    statuses = [req.status_code for req in reqs]
    content_types = [req.headers['content-type'] for req in reqs]
    
    for endpoint, status in zip(endpoints, statuses):
        assert status != 404, endpoint
    
    #assert set(statuses) == { 200 }
    #assert set(content_types) == { 'application/json' }
