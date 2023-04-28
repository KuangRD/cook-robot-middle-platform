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
        for seasoning in seasonings:
            res.append(seasoning.to_dict(["id", "name", "slot"]))
        return res

