import base64
from time import time
from uuid import uuid1
from sqlite_db import db


def timestamp():
    return int(time())


class BaseDbModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.Integer, nullable=False, default=timestamp())
    updated_at = db.Column(db.Integer, nullable=False, default=timestamp(),
                           onupdate=timestamp())

    def __init__(self):
        self.id = str(uuid1)

    def to_dict(self, columns=[]):
        model_dict = {}
        model_dict.update(self.__dict__)
        if "_sa_instance_state" in model_dict:
            del model_dict['_sa_instance_state']
        for k in list(model_dict):
            if k not in columns:
                del model_dict[k]
                continue
            # if k == "image":
            #     if model_dict[k] is not None:
            #         model_dict[k] = "data:image/png;base64," + base64.b64encode(model_dict[k]).decode("utf8")
        return model_dict
