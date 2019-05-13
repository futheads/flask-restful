from datetime import datetime

from flask_api.database import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return "<Post %r>" % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category %r>" % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(11), index=True)
    password = db.Column(db.String(30))
    nickname = db.Column(db.String(30), index=True, nullable=True)
    register_time = db.Column(db.DateTime)

    def __init__(self, phone_number, password, nickname, register_time):
        self.phone_number = phone_number
        self. password = password
        self.nickname = nickname
        self.register_time = nickname

    def __repr__(self):
        return "<User %r>" % self.nickname
