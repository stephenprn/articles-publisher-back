from sqlalchemy.orm import load_only

from models.user import User
from shared.db import db
from utils.utils_hash import check_password, hash_password
from shared.annotations import to_json


def authenticate(username: str, password: str):
    password_hashed = hash_password(password)

    user = db.session.query(User).options(load_only(
        'password',
        'salt'
    )).filter_by(
        username=username
    ).first()

    if user == None:
        return None

    if not check_password(password, user.salt, user.password):
        return None

    # prevent password and salt to be accessible after authentication
    db.session.expire(user)

    return user


def identity(payload):
    user_id = payload['identity']

    user = db.session.query(User).filter_by(
        id=user_id
    ).first()

    # prevent password and salt to be accessible after authentication
    db.session.expire(user)

    return user
