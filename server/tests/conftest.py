import sys
import os
import pytest
from xprocess import ProcessStarter
import requests
import shutil

ENV_FILE = os.path.realpath('test.env')
os.environ['ENV_FILE'] = ENV_FILE

from arlo_st.env import FS_ROOT, DATABASE
from arlo_st.db import create_tables

from fake_arlo import Arlo as FakeArlo
fake_arlo_client = FakeArlo("foo", "bar")

@pytest.fixture()
def fs_root():
    return os.environ['FS_ROOT']

@pytest.fixture()
def arlo_client():
    return fake_arlo_client

@pytest.fixture(scope='module')
def base_url():
    return f"http://localhost:5000"

@pytest.fixture
def get(base_url):
    def do_get(*subpaths):
        return requests.get(''.join([base_url] + list(subpaths)))
    return do_get

@pytest.fixture(scope='module')
def post(base_url):
    def do_post(*subpaths, json = {}):
        return requests.post(''.join([base_url] + list(subpaths)), json = json)
    return do_post

@pytest.fixture(scope='module')
def auth_creds(post):
    credentials = {
        "username": "test",
        "password": "foobar"
    }
    
    r = post('/register', json=credentials)
    return credentials

@pytest.fixture(scope='module')
def jwt_token(auth_creds, post):
    r = post('/login', json=auth_creds)
    return r.json()['access_token']

@pytest.fixture(scope='module')
def auth_get(base_url, jwt_token):
    def do_get(*subpaths):
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
        return requests.get(''.join([base_url] + list(subpaths)), headers=headers)
    return do_get

@pytest.fixture(scope='module')
def auth_post(base_url, jwt_token):
    def do_post(*subpaths, json={}):
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
        return requests.post(
            ''.join([base_url] + list(subpaths)),
            headers=headers,
            json = json
        )
    return do_post

@pytest.fixture(scope='module', autouse=True)
def clean_files():
    def rm_if_exists(path, rmFn=os.remove):
        try:
            rmFn(path)
        except FileNotFoundError:
            pass
        
    rm_if_exists(FS_ROOT, shutil.rmtree)
    rm_if_exists(DATABASE, os.remove)

# by "autousing" this fixture and scoping it to module, we are
# essentially cleaning the database
@pytest.fixture(scope='module', autouse=True)
def init_db(clean_files):
    create_tables()

# this xprocess thing is pretty funny... it's a fixture that starts a
# subprocess using ProcessStarter.args, and proceeds to run until
# ProcessStarter.pattern is matched against the first N lines of its
# stdout (by default N=50). I don't see a way to handle timeouts using
# the fixture, but we should be able to timeout the tests themselves.
@pytest.fixture(scope='module', autouse=True)
def flask_server(xprocess, init_db):
    arlo_st_server = "arlo_st_server"
    arlo_st_env = {
        "ENV_FILE": ENV_FILE
    }
    arlo_st_main = os.path.realpath('main.py')
    python_bin = sys.executable

    class Starter(ProcessStarter):
        pattern = "Running"
        args = [python_bin, arlo_st_main]
        env = arlo_st_env
    
    xprocess.ensure(arlo_st_server, Starter)
    yield
    xprocess.getinfo(arlo_st_server).terminate()

@pytest.fixture(scope='module')
def fake_arlo_server(xprocess):
    process_name = "fake_arlo_server"
    class Starter(ProcessStarter):
        pattern = "Running"
        args = ['fake_arlo_server']

    xprocess.ensure(process_name, Starter)
    yield
    xprocess.getinfo(process_name).terminate()

    
