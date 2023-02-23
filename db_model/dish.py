from sqlite_db import db
from db_model.base import BaseDbModel


class DishDbModel(BaseDbModel):
    __tablename__ = "dishes"
    name = db.Column(db.String, nullable=False, default="")
    initials = db.Column(db.String, nullable=False, default="")
    cook_time = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String, nullable=False, default="")
    is_starred = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, initials, cook_time, image):
        super(DishDbModel, self).__init__()
        self.name = name
        self.initials = initials
        self.cook_time = cook_time
        self.image = image
        self.is_starred = 0

    def __repr__(self):
        return '<Dish %r>' % self.name
