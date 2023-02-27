from flask_restful import Resource, reqparse
from db_model.stir_fry import StirFryDbModel
from sqlite_db import db


class StirFries(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        res = []
        seasonings = db.session.execute(
            db.select(StirFryDbModel).order_by(StirFryDbModel.tag.asc())).scalars()
        for ing in seasonings:
            res.append(ing.to_dict(["id", "name", "tag"]))
        return res

