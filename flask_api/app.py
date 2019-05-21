import os
import logging.config

from flask import Flask, Blueprint
from flask_api.database import db, redis_store
from flask_api.config import configs
from flask_api.api.restplus import api

app = Flask(__name__)

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "logging.ini"))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config["SERVER_NAME"] = configs["flask_server_name"]
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = configs["db"]["sqlalchemy_database_uri"]
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = configs["db"]["sqlalchemy_track_modifications"]
    flask_app.config["REDIS_URL"] = configs["db"]["redis_url"]

    flask_app.config["SWAGGER_UI_DOC_EXPANSION"] = configs["flaskplus"]["restplus_swagger_ui_doc_expansion"]
    flask_app.config["RESTPLUS_VALIDATE"] = configs["flaskplus"]["restplus_validate"]
    flask_app.config["RESTPLUS_MASK_SWAGGER"] = configs["flaskplus"]["restplus_mask_swagger"]
    flask_app.config["ERROR_404_HELP"] = configs["flaskplus"]["restplus_error_404_help"]


def initialize_app(flask_app):
    from flask_api.api.blog.endpoints import posts, categories
    from flask_api.api.user.endpoints import user
    from flask_api.api.commons.endpoints import common
    configure_app(flask_app)

    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    db.init_app(flask_app)
    redis_store.init_app(app)


def main():
    initialize_app(app)
    # log.info(">>>>> Starting development server at http://{}/api/ <<<<<".format(app.config["SERVER_NAME"]))


main()
