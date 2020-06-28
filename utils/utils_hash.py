import os
import hashlib
from base64 import b64decode, b64encode


def generate_random_salt():
    return os.urandom(32)


def hash_password(password: str):
    salt = b64encode(generate_random_salt())
    password_hashed = b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    ))

    return (password_hashed, salt)


def check_password(pw_input: str, salt: str, pw_hashed: str):
    pw_input_hashed = b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        pw_input.encode('utf-8'),  # Convert the password to bytes
        salt.encode('utf-8'),
        100000
    ))

    return pw_hashed == pw_input_hashed
