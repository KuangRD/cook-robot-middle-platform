from flask_restful import Resource, reqparse
from db_model.seasoning import SeasoningDbModel
from sqlite_db import db


class Seasonings(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        res = []
        seasonings = db.session.execute(
            db.select(SeasoningDbModel).order_by(SeasoningDbModel.updated_at.desc())).scalars()
        for ing in seasonings:
            res.append(ing.to_dict(["id", "name"]))
        return res

