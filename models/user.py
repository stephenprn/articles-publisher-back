from sqlalchemy import inspect
from uuid import uuid4

from shared.db import db
from utils import utils_date, utils_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), unique=True, nullable=False)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.VARBINARY(128), nullable=False)
    salt = db.Column(db.VARBINARY(32), nullable=False)

    creation_date = db.Column(
        db.DateTime, default=utils_date.get_current_date(), nullable=False)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email

        pw_salt = utils_hash.hash_password(password)

        self.password = pw_salt[0]
        self.salt = pw_salt[1]

        self.uuid = str(uuid4())

    def __repr__(self):
        state = inspect(self)

        def ga(attr):
            return (repr(getattr(self, attr))
                    if attr not in state.unloaded
                    else "<deferred>")

        attrs = " ".join([f"{attr.key}={ga(attr.key)}"
                          for attr in state.attrs])
        return f"<User {attrs}>"

    def to_dict(self):
        state = inspect(self)

        # add property to dict only if column is loaded (can be excluded with load_only)
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != 'id' and c.name not in state.unloaded
        }
