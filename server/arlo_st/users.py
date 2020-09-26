from hashlib import scrypt
from os import urandom
import base64
from peewee import IntegrityError
from arlo_st.db import User

class IncorrectPassword(Exception):
    pass

class UserNotFound(Exception):
    pass

class UserEExist(Exception):
    pass

# if user not found, simply switch exceptions around... this
# is just for the convenience of only having to check exceptions
# in a single module (the current one)
def get(username):
    try:
        return User.get(User.username == username)
    except User.DoesNotExist:
        raise UserNotFound()

def preparramed_scrypt(password, *, salt):
    return scrypt(password, salt=salt, n=2, r=16, p=1)

def raise_authenticate(user, password):
    [b64_hashed, b64_salt] = user.password.split('.')

    hashed = base64.b64decode(b64_hashed)
    salt = base64.b64decode(b64_salt)

    b_password = bytearray(password, "utf8") 
    
    if preparramed_scrypt(b_password, salt=salt) != hashed:
        raise IncorrectPassword()

def register(username, password):
    # convert string password to bytearray
    b_password = bytearray(password, "utf8")

    # generate 32 bytes of random string
    salt = urandom(32)

    # hash using scrypt
    # [!] see hashlib docs for param meaning
    hashed = preparramed_scrypt(b_password, salt=salt)

    # encode to base64 to get ascii
    b64_hashed = base64.b64encode(hashed)
    b64_salt = base64.b64encode(salt)
    
    # concatenate hash and salt together
    # this is what we store in the db
    cypher_password = '.'.join([b64_hashed.decode(), b64_salt.decode()])

    try:
        return User.create(username=username, password=cypher_password)
    except IntegrityError:
        raise UserEExist()
