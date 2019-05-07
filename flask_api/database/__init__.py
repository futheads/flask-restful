from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from flask_api.database.models import Post, Category
    db.drop_all()
    db.create_all()
