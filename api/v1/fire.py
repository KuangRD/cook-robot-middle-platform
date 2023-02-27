from flask_restful import Resource, reqparse
from db_model.fire import FireDbModel
from sqlite_db import db


class Fires(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        res = []
        fires = db.session.execute(
            db.select(FireDbModel).order_by(FireDbModel.tag.asc())).scalars()
        for ing in fires:
            res.append(ing.to_dict(["id", "name", "tag"]))
        return res

