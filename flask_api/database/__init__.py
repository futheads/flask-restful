from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

db = SQLAlchemy()
redis_store = FlaskRedis(decode_responses=True)


def reset_database():
    from flask_api.database.models import Post, Category
    db.drop_all()
    db.create_all()
