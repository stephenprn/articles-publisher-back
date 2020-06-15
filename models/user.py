from shared.db import db
from utils import utils_date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, default=utils_date.get_current_date(), nullable=False)

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def to_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }
