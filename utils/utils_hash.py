import os
import hashlib
from base64 import b64decode, b64encode


def generate_random_salt():
    return os.urandom(32)


def hash_password(password: str):
    salt = str(b64encode(generate_random_salt()))

    password_hashed = __hash_pw_salt(password, salt)

    return (password_hashed, salt)


def check_password(pw_input: str, salt: str, pw_hashed: str):
    pw_input_hashed = __hash_pw_salt(pw_input, salt)

    return pw_hashed == pw_input_hashed


def __hash_pw_salt(password: str, salt: str):
    return str(b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Convert the password to bytes
        salt.encode('utf-8'),
        100000
    )))
