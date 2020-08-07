import pytest
import sys
from xprocess import ProcessStarter
import os
import requests

ENV_FILE = os.path.realpath('test.env')
os.environ['ENV_FILE'] = ENV_FILE

from arlo_st.env import FS_ROOT, DATABASE
from arlo_st.db import create_tables

from fake_arlo import Arlo as FakeArlo
fake_arlo_client = FakeArlo("foo", "bar")

@pytest.fixture()
def arlo_client():
    return fake_arlo_client

#just testing out fixtures
@pytest.fixture
def foo():
    return 1

@pytest.fixture
def base_url():
    return f"http://localhost:5000"

@pytest.fixture
def get(base_url):
    def do_get(*subpaths):
        return requests.get(''.join([base_url] + list(subpaths)))
    return do_get

@pytest.fixture
def post(base_url):
    def do_post(*subpaths, json = {}):
        return requests.post(''.join([base_url] + list(subpaths)), json = json)
    return do_post

@pytest.fixture(scope='module', autouse=True)
def clean_files():
    try:
        os.rmdir(FS_ROOT)
        os.remove(DATABASE)
    except FileNotFoundError:
        pass

@pytest.fixture(scope='module', autouse=True)
def init_db(clean_files):
    create_tables()
    

#this xprocess thing is pretty funny... it's a fixture that starts a
#subprocess using ProcessStarter.args, and proceeds to run until
#ProcessStarter.pattern is matched against the first N lines of its
#stdout (by default N=50). I don't see a way to handle timeouts using
#the fixture, but we should be able to timeout the tests themselves.
@pytest.fixture(scope='module', autouse=True)
def flask_server(xprocess, init_db):
    arlo_st_server = "arlo_st_server"
    arlo_st_env = {
        "ENV_FILE": ENV_FILE
    }
    arlo_st_main = os.path.realpath('main.py')
    python_bin = sys.executable

    class Starter(ProcessStarter):
        pattern="Running"
        args = [python_bin, arlo_st_main]
        env = arlo_st_env
    
    logfile = xprocess.ensure(arlo_st_server, Starter)
    yield
    xprocess.getinfo(arlo_st_server).terminate()

