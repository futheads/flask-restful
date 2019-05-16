import logging
import hashlib
import time

from flask import request
from flask_restplus import Resource
from flask_api.api.user.serializers import login_req, login_resp, current_user_resp

from flask_api.api.restplus import NotFoundError, ValidationError, api, login_check, BaseResponse, base_model, \
    log_record
from flask_api.database.models import User
from flask_api.database import redis_store


log = logging.getLogger(__name__)

ns = api.namespace("", description="Operations related to login")


@ns.route("/login")
@api.response(404, "没有此用户")
@api.response(400, "密码错误")
class UserLogin(Resource):

    @api.doc(security=None)
    @log_record
    @api.expect(login_req)
    @api.marshal_with(login_resp)
    def post(self):
        """
        user login.
        """
        data = request.json
        phone_number = data.get("phone_number")
        password = data.get("password")
        user = User.query.filter(User.phone_number == phone_number).one()
        if not user:
            raise NotFoundError("没有此用户")
        if user.password != password:
            raise ValidationError("密码错误")
        m = hashlib.md5()
        m.update(phone_number.encode("utf-8"))
        m.update(password.encode("utf-8"))
        m.update(str(int(time.time())).encode("utf-8"))
        token = m.hexdigest()

        pipeline = redis_store.pipeline()
        pipeline.hmset("user:%s" % user.phone_number, {"token": token, "nickname": user.nickname, "app_online": 1})
        pipeline.set("token:%s" % token, user.phone_number)
        pipeline.expire("token:%s" % token, 3600*24*30)
        pipeline.execute()
        return BaseResponse({"nickname": user.nickname, "token": token}, message="成功登录")


@ns.route("/user")
class UserInfo(Resource):

    @log_record
    @login_check
    @api.marshal_with(current_user_resp)
    def get(self):
        """
        get current user
        :return:
        """
        token = request.headers.get("token")
        phone_number = redis_store.get("token:%s" % token)
        nickname = redis_store.hget("user:%s" % phone_number, "nickname")
        return BaseResponse({"nickname": nickname, "phone_number": phone_number})


@ns.route("/logout")
class Logout(Resource):

    @log_record
    @login_check
    @api.marshal_with(base_model)
    def post(self):
        """
        user logout
        :return:
        """
        token = request.headers.get("token")
        phone_number = redis_store.get("token:%s" % token)
        pipeline = redis_store.pipeline()
        pipeline.delete("token:%s" % token)
        pipeline.hmset("user:%s" % phone_number, {"app_online": 0})
        pipeline.execute()
        return BaseResponse(None, message="注销成功")

