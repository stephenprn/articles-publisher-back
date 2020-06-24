from sqlalchemy import inspect
from sqlalchemy.orm import relationship
from uuid import uuid4

from shared.db import db
from utils import utils_date, utils_hash


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), unique=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text)
    url = db.Column(db.String(100), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="articles")

    creation_date = db.Column(
        db.DateTime, default=utils_date.get_current_date(), nullable=False)

    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body
        self.uuid = str(uuid4())

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

        # load of non-relationship properties
        # add property to dict only if column is loaded (can be excluded with load_only)
        res = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != 'id' and c.name not in state.unloaded
        }

        # load of relationship propeties
        for rel in state.mapper.relationships:
            key = rel.key

            print(key)
            print(state.unloaded)

            if key not in state.unloaded:
                res[key] = getattr(self, key).to_dict()

        print(res)

        return res
