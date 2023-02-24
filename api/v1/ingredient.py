from flask_restful import Resource, reqparse
from db_model.ingredient import IngredientDbModel, ShapeDbModel
from sqlite_db import db


class Ingredients(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        res = []
        ingredients = db.session.execute(
            db.select(IngredientDbModel).order_by(IngredientDbModel.updated_at.desc())).scalars()
        for ing in ingredients:
            res.append(ing.to_dict(["id", "name", "classification"]))
        return res


class Shapes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        res = []
        shapes = db.session.execute(
            db.select(ShapeDbModel).order_by(ShapeDbModel.updated_at.desc())).scalars()
        for shape in shapes:
            res.append(shape.to_dict(["id", "name"]))
        return res
