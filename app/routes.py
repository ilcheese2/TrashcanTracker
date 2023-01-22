import sqlalchemy

from app import app, db, waterfountainidx, trashcanidx
from flask import request, render_template
from app.models import Point
import requests


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_point():
    if not len(trashcanidx) + len(waterfountainidx) == Point.query.count():
        for i in range(trashcanidx.get_size()):
            trashcanidx.delete(i, None)
        for i in range(waterfountainidx.get_size()):
            waterfountainidx.delete(i, None)
        for point in Point.query.all():
            if point.type[0] == 0:
                trashcanidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
            else:
                waterfountainidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
    response = {"result": "success"}
    try:
        point = Point(id=Point.query.count(), **request.json)
        if point.type[0] == "0":
            if next(trashcanidx.intersection((-app.config.get("SPAM_RANGE") + point.latitude,
                                              -app.config.get("SPAM_RANGE") + point.longitude,
                                              app.config.get("SPAM_RANGE") + point.latitude,
                                              app.config.get("SPAM_RANGE") + point.longitude)), None) is None:
                db.session.add(point)
                db.session.commit()
                trashcanidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
            else:
                response = {"result": "spam"}
        else:
            if next(waterfountainidx.intersection((-app.config.get("SPAM_RANGE") + point.latitude,
                                                   -app.config.get("SPAM_RANGE") + point.longitude,
                                                   app.config.get("SPAM_RANGE") + point.latitude,
                                                   app.config.get("SPAM_RANGE") + point.longitude)), None) is None:
                db.session.add(point)
                db.session.commit()
                waterfountainidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
            else:
                response = {"result": "spam"}
    except TypeError:
        response = {"result": "invalid"}
    except sqlalchemy.exc.IntegrityError:
        response = {"result": "invalid"}
    return response


@app.route("/near", methods=["GET"])
def get_near_points():
    if not len(trashcanidx) + len(waterfountainidx) == Point.query.count():
        for i in range(trashcanidx.get_size()):
            trashcanidx.delete(i, None)
        for i in range(waterfountainidx.get_size()):
            waterfountainidx.delete(i, None)
        for point in Point.query.all():
            if point.type[0] == 0:
                trashcanidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
            else:
                waterfountainidx.insert(point.id, (point.latitude, point.longitude, point.latitude, point.longitude))
    point = Point(id=-1, latitude=float(request.args.get("latitude")), longitude=float(request.args.get("longitude")))
    data = []
    for i in trashcanidx.intersection(
            (-app.config.get("RANGE") + point.latitude, -app.config.get("RANGE") + point.longitude,
             app.config.get("RANGE") + point.latitude, app.config.get("RANGE") + point.longitude)):
        try:
            data.append(Point.query[i].to_list())
        except IndexError as e:
            print(i)
    for i in waterfountainidx.intersection(
            (-app.config.get("RANGE") + point.latitude, -app.config.get("RANGE") + point.longitude,
             app.config.get("RANGE") + point.latitude, app.config.get("RANGE") + point.longitude)):
        try:
            data.append(Point.query[i].to_list())
        except IndexError as e:
            print(i)
    return {"result": "success", "data": data}


@app.route("/map", methods=["GET"])
def get_map():
    return requests.get(
        "https://www.bing.com/maps/sdkrelease/mapcontrol?callback=GetMap&key=key").text
