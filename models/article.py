from sqlalchemy import inspect
from uuid import uuid4

from shared.db import db
from utils import utils_date, utils_hash


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), default=str(
        uuid4()), unique=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text)
    url = db.Column(db.String(100), unique=True, nullable=False)

    creation_date = db.Column(
        db.DateTime, default=utils_date.get_current_date(), nullable=False)

    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body

    def __repr__(self):
        state = inspect(self)

        def ga(attr):
            return (repr(getattr(self, attr))
                    if attr not in state.unloaded
                    else "<deferred>")

        attrs = " ".join([f"{attr.key}={ga(attr.key)}"
                          for attr in state.attrs])
        return f"<Article {attrs}>"

    def to_dict(self):
        state = inspect(self)

        # add property to dict only if column is loaded (can be excluded with load_only)
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != 'id' and c.name not in state.unloaded
        }
