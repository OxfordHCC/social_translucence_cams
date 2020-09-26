import os
import sys
from dotenv import load_dotenv
from pathlib import Path

P_ROOT = os.getenv("P_ROOT") or os.getcwd()
ENV_FILE = os.getenv("ENV_FILE") or '.env'

env_path = os.path.join(P_ROOT, ENV_FILE)

if(not os.path.isfile(env_path)):
    raise Exception(f"Invalid ENV_FILE value; {env_path} is not a file.")

load_dotenv(verbose=True, dotenv_path=env_path)

VERBOSE = os.getenv("VERBOSE") or True
#USERNAME = os.getenv("USERNAME")
#PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
DATABASE = os.path.join(P_ROOT, DATABASE)
FS_PATH = os.getenv("FS_PATH")
FS_ROOT = os.path.join(P_ROOT, FS_PATH)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

#We need to change the Arlo client to a fake one for integration
#testing purposes because we can't use a real one. "Why?" you might
#ask. We could... but Arlo seems to delete videos when the month
#passes, so there's a high chance that we'd test with empty arrays. I
#think a full test includes test with data. Ideally, we would test
#both cases (once with real and once with fake).
ARLO_MODULE = os.getenv("ARLO_CLIENT") or "arlo"

#oh lord, forgive me...
Arlo = __import__(ARLO_MODULE, globals(), locals(), ['Arlo']).Arlo

#TOOD: print every env variable, but not manually. Find better way to do it
if(VERBOSE is True):
    print(f"ENV_FILE is {ENV_FILE}")
    print(f"FS_ROOT is {FS_ROOT}")
    print(f"DATABASE is {DATABASE}")


