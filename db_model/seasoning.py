from sqlite_db import db
from db_model.base import BaseDbModel


class SeasoningDbModel(BaseDbModel):
    __tablename__ = "seasonings"
    name = db.Column(db.String, nullable=False, default="")
    slot = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, slot):
        super(SeasoningDbModel, self).__init__()
        self.name = name
        self.slot = slot

    def __repr__(self):
        return '<Seasoning %r>' % self.name

