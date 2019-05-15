import logging
import hashlib
import time

from flask import request
from flask_restplus import Resource
from flask_api.api.user.serializers import login

from flask_api.api.restplus import api, login_check
from flask_api.database.models import User
from flask_api.database import redis_store


log = logging.getLogger(__name__)

ns = api.namespace("", description="Operations related to login")


@ns.route("/login")
class UserLogin(Resource):

    @api.doc(security=None)
    @api.expect(login)
    def post(self):
        """
        user login.
        """
        data = request.json
        phone_number = data.get("phone_number")
        password = data.get("password")
        user = User.query.filter(User.phone_number == phone_number).one()
        if not user:
            return {"code": 0, "message": "没有此用户"}
        if user.password != password:
            return {"code": 0, "message": "密码错误"}
        m = hashlib.md5()
        m.update(phone_number.encode("utf-8"))
        m.update(password.encode("utf-8"))
        m.update(str(int(time.time())).encode("utf-8"))
        token = m.hexdigest()
        redis_store.hmset("user:%s" % user.phone_number, {"token": token, "nickname": user.nickname, "app_online": 1})
        redis_store.set("token:%s" % token, user.phone_number)
        redis_store.expire("token:%s" % token, 3600*24*30)
        return {"code": 1, "message": "成功登录", "nickname": user.nickname, "token": token}


@ns.route("/user")
class UserInfo(Resource):

    @login_check
    def get(self):
        """
        get current user
        :return:
        """
        token = request.headers.get("token")
        phone_number = redis_store.get("token:%s" % token)
        nickname = redis_store.hget("user:%s" % phone_number, "nickname")
        return {"code": 1, "nickname": nickname, "phone_number": phone_number}


@ns.route("/logout")
class Logout(Resource):

    @login_check
    def post(self):
        """
        user logout
        :return:
        """
        token = request.headers.get("token")
        phone_number = redis_store.get("token:%s" % token)
        redis_store.delete("token:%s" % token)
        redis_store.hmset("user:%s" % phone_number, {"app_online": 0})
        return {"code": 1, "message": "成功注销"}
