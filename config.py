import os
import pathlib


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(pathlib.Path(__file__).parent.resolve(), "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RANGE = 0.003
    SPAM_RANGE = 0.0001
