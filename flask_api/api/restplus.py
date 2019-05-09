import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from flask_api.config import configs
from flask_api.api.errors import ServerError, NotFoundError, NotAuthorizedError, ValidationError, DatabaseNotFoundError

log = logging.getLogger(__name__)

api = Api(version="1.0", title="Micro Blog API",
          description="A simple demonstration of a Flask RestPlus powered API")


@api.errorhandler(NotFoundError)
@api.errorhandler(NotAuthorizedError)
@api.errorhandler(ValidationError)
def handle_error(error):
    return error.to_dict(), getattr(error, "code")


@api.errorhandler
def default_error_handler(error):
    """Returns Internal server error"""
    log.exception(error)
    error = ServerError()
    if not configs["flask_debug"]:
        return error.to_dict(), getattr(error, "code", 500)


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(error):
    log.warning(traceback.format_exc())
    error = DatabaseNotFoundError()
    return error.to_dict(), getattr(error, "code", 404)
