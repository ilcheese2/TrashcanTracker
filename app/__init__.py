from flask import Flask
from flask_cors import CORS

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from rtree import index
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
trashcanidx = index.Index()
waterfountainidx = index.Index()

from app import routes, models
from app.models import Point

app.app_context().push()

for point in Point.query.all():
    if point.type[0] == 0:
        trashcanidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
    else:
        waterfountainidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
