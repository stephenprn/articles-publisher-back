import os
import hashlib


def generate_random_salt():
    return os.urandom(32)


def hash_password(password: str):
    salt = generate_random_salt()
    password_hashed = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

    return (password_hashed, salt)


def check_password(pw_input: str, salt: str, pw_hashed: str):
    pw_input_hashed = hashlib.pbkdf2_hmac(
        'sha256',
        pw_input.encode('utf-8'),  # Convert the password to bytes
        salt,
        100000
    )

    return pw_hashed == pw_input_hashed