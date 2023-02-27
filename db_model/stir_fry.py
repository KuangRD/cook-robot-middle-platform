from sqlite_db import db
from db_model.base import BaseDbModel


class StirFryDbModel(BaseDbModel):
    __tablename__ = "stirFries"
    name = db.Column(db.String, nullable=False, default="")
    tag = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, tag):
        super(StirFryDbModel, self).__init__()
        self.name = name
        self.tag = tag

    def __repr__(self):
        return '<StirFry %r>' % self.name
