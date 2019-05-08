import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from flask_api.config import configs
from flask_api.api.errors import APIValueError, APIResourceNotFound, APIPermissionError
from flask_restplus import abort

log = logging.getLogger(__name__)

api = Api(version="1.0", title="Micro Blog API",
          description="A simple demonstration of a Flask RestPlus powered API")


@api.errorhandler(APIValueError)
def default_error_handler(error):
    print("--------------------------")
    print(error.error)
    print(error.data)
    print(error.message)
    print("--------------------------")
    # return {"error": error.error, "data": error.data, "message": error.message}, 500
    abort(500, {"error": error.error, "data": error.data, "message": error.message})


@api.errorhandler
def default_error_handler(error):
    message = "An unhandled exception occurred."
    log.exception(message)
    if not configs["flask_debug"]:
        return {"error": "exception:unhandled", "data": str(error), "message": message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(error):
    log.warning(traceback.format_exc())
    return {"error": "database:not_found", "data": str(error),
            "message": "A database result was required but none was found."}, 500
