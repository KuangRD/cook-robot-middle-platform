import base64
import json

from flask_restful import Resource, fields, marshal_with, reqparse
from db_model.dish import DishDbModel
from sqlite_db import db
from pypinyin import pinyin, FIRST_LETTER


class Dish(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'name',
            type=str,
            location='json',
        )
        self.parser.add_argument(
            'cook_time',
            type=str,
            location='json',
        )
        self.parser.add_argument(
            'dish',
            type=dict,
            location='json',
        )

    def get(self, dish_id):
        res = None
        dish = db.session.execute(db.select(DishDbModel).where(DishDbModel.id == dish_id)).scalar_one_or_none()
        if dish is not None:
            res = dish.to_dict(["id", "name", "image", "cook_time", "is_starred"])
        return res

    def post(self):  # 创建单条
        args = self.parser.parse_args()
        name = args.get("name")
        cook_time = args.get("cook_time")
        initials_list = pinyin(name, style=FIRST_LETTER)
        initials = ""
        for i in initials_list:
            initials += i[0]
        dish = DishDbModel(name, initials, cook_time)
        db.session.add(dish)
        db.session.commit()

    def put(self, dish_id):
        args = self.parser.parse_args()
        new_dish = args.get("dish")
        name = new_dish["name"]
        # image = base64.b64decode(new_dish["image"].replace("data:image/png;base64,", ""))
        image = new_dish["image"]
        is_starred = new_dish["is_starred"]
        try:
            result = db.session.execute(db.update(DishDbModel).where(DishDbModel.id == dish_id).values(
                name=name,
                image=image,
                is_starred=is_starred
            ))
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        db.session.commit()
        return True


class Dishes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'page_size',
            type=int,
            location='args',
        )
        self.parser.add_argument(
            'page_index',
            type=int,
            location='args',
        )

    def get(self, initials=""):
        args = self.parser.parse_args()
        page_size = args.get("page_size")
        page_index = args.get("page_index")
        res = []
        if initials == "":  # 分页查询所有
            dishes = db.session.execute(
                db.select(DishDbModel).order_by(
                    DishDbModel.updated_at.desc()).limit(page_size).offset(
                    (page_index - 1) * page_size)).scalars()
        else:  # 分页查询首字母符合
            dishes = db.session.execute(
                db.select(DishDbModel).where(
                    DishDbModel.initials.like("%" + initials + "%")).order_by(
                    DishDbModel.updated_at.desc()).limit(page_size).offset(
                    (page_index - 1) * page_size)).scalars()
        for d in dishes:
            res.append(d.to_dict(["id", "name", "image", "initials"]))
        return res


class StarredDishes(Dishes):
    def __init__(self):
        super(StarredDishes, self).__init__()

    def get(self, initials=""):
        args = self.parser.parse_args()
        page_size = args.get("page_size")
        page_index = args.get("page_index")
        res = []
        if initials == "":  # 分页查询所有
            dishes = db.session.execute(
                db.select(DishDbModel).where(DishDbModel.is_starred == 1).order_by(
                    DishDbModel.updated_at.desc()).limit(page_size).offset(
                    (page_index - 1) * page_size)).scalars()
        else:  # 分页查询首字母符合
            dishes = db.session.execute(
                db.select(DishDbModel).where(DishDbModel.is_starred == 1).where(
                    DishDbModel.initials.like("%" + initials + "%")).order_by(
                    DishDbModel.updated_at.desc()).limit(page_size).offset(
                    (page_index - 1) * page_size)).scalars()
        for d in dishes:
            res.append(d.to_dict(["id", "name", "image", "initials"]))
        return res


class DishesCount(Resource):
    def __init__(self):
        super(DishesCount, self).__init__()

    def get(self, initials=""):
        if initials == "":  # 查询所有总数
            dishes_table = db.table('dishes', db.column('id'))
            dishes_count = db.session.execute(db.select(db.func.count("id")).select_from(dishes_table)).first()[0]
        else:  # 查询首字母符合总数
            dishes_table = db.table('dishes', db.column('id'), db.column('initials'))
            dishes_count = db.session.execute(
                db.select(db.func.count("id")).where(dishes_table.c.initials.like("%" + initials + "%")).select_from(
                    dishes_table)).first()[0]
        return dishes_count


class StarredDishesCount(Resource):
    def __init__(self):
        super(StarredDishesCount, self).__init__()

    def get(self, initials=""):
        if initials == "":  # 查询所有总数
            dishes_table = db.table('dishes', db.column('id'), db.column('is_starred'))
            dishes_count = db.session.execute(
                db.select(db.func.count("id")).where(
                    dishes_table.c.is_starred == 1).select_from(dishes_table)).first()[0]
        else:  # 查询首字母符合总数
            dishes_table = db.table('dishes', db.column('id'), db.column('is_starred'), db.column('initials'))
            dishes_count = db.session.execute(
                db.select(db.func.count("id")).where(dishes_table.c.is_starred == 1).where(
                    dishes_table.c.initials.like("%" + initials + "%")).select_from(
                    dishes_table)).first()[0]
        return dishes_count
