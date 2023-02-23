import os
from flask_sqlalchemy import SQLAlchemy

dir_path = os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy()


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + dir_path + "/crs.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
