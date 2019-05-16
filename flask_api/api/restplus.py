import logging
import traceback
from functools import wraps

from flask import request
from flask_restplus import Api, fields
from sqlalchemy.orm.exc import NoResultFound
from flask_api.config import configs
from flask_api.api.errors import ServerError, NotFoundError, NotAuthorizedError, ValidationError, DatabaseNotFoundError
from flask_api.database import redis_store

log = logging.getLogger(__name__)

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "token"
    },
}

api = Api(security="Bearer Auth", authorizations=authorizations, version="1.0", title="Micro Blog API",
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


base_model = api.model("base response model", {
    "code": fields.Integer(readOnly=True, description="response status code", default=200),
    "message": fields.String(readOnly=True, default="请求成功"),
    "status": fields.String(readOnly=True, default="SUCCESS"),
})


class BaseResponse:
    """
    response 基类
    """
    def __init__(self, data, code=200, message="请求成功", status="SUCCESS"):
        self.data = data
        self.code = code
        self.message = message
        self.status = status


def login_check(f):
    """token 检查"""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            raise NotAuthorizedError("需要验证")

        phone_number = redis_store.get("token:%s" % token)
        if not phone_number or token != redis_store.hget("user:%s" % phone_number, "token"):
            raise NotAuthorizedError("验证信息错误")
        return f(*args, **kwargs)
    return decorator


def log_record(f):
    """记录日志"""
    @wraps(f)
    def decorator(*args, **kwargs):
        log.info("Request url: %s %s" % (request.method, request.path))
        log.info("Request args: %s" % request.args)
        log.info("Request body: %s" % request.json)
        response = f(*args, **kwargs)
        log.info("Response: %s" % response)
        return response
    return decorator
