import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from flask_api import config

log = logging.getLogger(__name__)

api = Api(version="1.0", title="Micro Blog API",
          description="A simple demonstration of a Flask RestPlus powered API")


@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    log.exception(message)

    if not config.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
