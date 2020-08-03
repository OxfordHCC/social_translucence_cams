from setuptools import setup

#this is copied from github.com/jeffreydwalter/arlo setup.py
def readme():
    with open('Readme.md') as desc:
        return desc.read()

setup(
    name='fake_arlo',
    py_modules=['fake_arlo'],
    version='0.0.1',
    description="A fake arlo client, mocking the one at github.com/jeffreydwalter/arlo setup.py",
    pacakge_data = {
        "": ["*.json"]
    },
    url="n/a"
)
