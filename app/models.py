from app import db


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Id: {self.id}, Pos: ({self.latitude}, {self.longitude}), Type: {self.type}"

    def to_list(self):
        return [self.latitude, self.longitude, self.type, self.id]