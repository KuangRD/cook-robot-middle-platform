from sqlite_db import db
from db_model.base import BaseDbModel


class SeasoningDbModel(BaseDbModel):
    __tablename__ = "seasonings"
    name = db.Column(db.String, nullable=False, default="")

    def __init__(self, name):
        super(SeasoningDbModel, self).__init__()
        self.name = name

    def __repr__(self):
        return '<Seasoning %r>' % self.name

