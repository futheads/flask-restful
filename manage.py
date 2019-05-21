import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_api.app import app
from flask_api.database import db

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "flask_api", "db.sqlite")
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
