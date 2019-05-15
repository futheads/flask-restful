from flask_api.database import db
from flask_api.database.models import User


def create_user(data):
    phone_number = data.get("phone_number")
    password = data.get("password")
    nickname = data.get("nickname")
    user = User(phone_number, password, nickname)
    db.session.add(user)
    db.session.commit()


def update_user(user_id, data):
    user = User.query.filter(User.id == user_id).one()
    user.phone_number = data.get("phone_number")
    user.password = data.get("password")
    user.nickname = data.get("nickname")
    db.session.add(user)
    db.session.commit()


def delete_user(user_id):
    user = User.query.filter(User.id == user_id).one()
    db.session.delete(user)
    db.session.commit()
