from sqlite_db import db
from db_model.base import BaseDbModel


class FireDbModel(BaseDbModel):
    __tablename__ = "fires"
    name = db.Column(db.String, nullable=False, default="")
    tag = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, tag):
        super(FireDbModel, self).__init__()
        self.name = name
        self.tag = tag

    def __repr__(self):
        return '<Fire %r>' % self.name

