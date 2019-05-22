import logging
import time
import hashlib
import random
import uuid

from flask import request, g
from flask_restplus import Resource
from qiniu import Auth

from flask_api.api.commons.serializers import login_req, login_resp, phone_number_field, current_user_resp, \
    qiniu_token_resp
from flask_api.api.restplus import api, login_check, log_record, BaseResponse, base_model
from flask_api.api.errors import NotFoundError, ValidationError, SMSError
from flask_api.database.models import User
from flask_api.database import redis_store
from flask_api.api.utils import send_sms, encrypted_password
from flask_api.config import configs


log = logging.getLogger(__name__)

ns = api.namespace("common", description="Operations related to common")

access_key = configs["qiniu"]["access_key"]
secret_key = configs["qiniu"]["secret_key"]
bucket_name = configs["qiniu"]["bucket_name"]

qiniu_auth = Auth(access_key, secret_key)


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
        if user.password != encrypted_password(password):
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
        user = g.current_user
        nickname = redis_store.hget("user:%s" % user.phone_number, "nickname")
        return BaseResponse({"nickname": nickname, "phone_number": user.phone_number})


@ns.route("/logout")
class Logout(Resource):

    @log_record
    @login_check
    @api.marshal_with(base_model)
    def put(self):
        """
        user logout
        :return:
        """
        user = g.current_user
        pipeline = redis_store.pipeline()
        pipeline.delete("token:%s" % g.token)
        pipeline.hmset("user:%s" % user.phone_number, {"app_online": 0})
        pipeline.execute()
        return BaseResponse(None, message="注销成功")


@ns.route("/smsend")
@api.response(400, "该用户已经存在,注册失败")
@api.response(500, "短信服务不可用")
class SMSend(Resource):
    """
    发送短信验证
    """
    @api.doc(security=None)
    @log_record
    @api.expect(phone_number_field)
    @api.marshal_with(base_model)
    def post(self):
        phone_number = request.json.get("phone_number")
        user = User.query.filter_by(phone_number=phone_number).first()

        if user:
            raise ValidationError("phone_number", message="该用户已经存在,注册失败")
        validate_number = str(random.randint(100000, 1000000))
        result, err_message = send_sms(phone_number, validate_number)

        if not result:
            raise SMSError("short message send fail")

        pipeline = redis_store.pipeline()
        pipeline.set("validate:%s" % phone_number, validate_number)
        pipeline.expire("validate:%s" % phone_number, 60)
        pipeline.execute()

        return BaseResponse(None, message="发送成功")


@ns.route("/smvalidate")
@api.response(400, "验证码错误")
class SMValidate(Resource):
    """
    验证短信
    """
    @api.doc(security=None)
    @log_record
    @api.expect()
    @api.marshal_with(base_model)
    def post(self):
        data = request.json
        phone_number = data.get("phone_number")
        validate_number = data.get("validate_number")
        validate_number_in_redis = redis_store.get("validate:%s" % phone_number)

        if validate_number != validate_number_in_redis:
            raise ValidationError("validate_number", message="验证码错误")

        pipe_line = redis_store.pipeline()
        pipe_line.set("is_validate:%s" % phone_number, "1")
        pipe_line.expire("is_validate:%s" % phone_number, 120)
        pipe_line.execute()

        return BaseResponse(None, message="短信验证通过")


@ns.route("/qiniu_token")
class QiniuToken(Resource):
    """
    获取七牛上传授权
    """
    @log_record
    @login_check
    @api.expect()
    @api.marshal_with(qiniu_token_resp)
    def get(self):
        key = uuid.uuid4()
        token = qiniu_auth.upload_token(bucket_name, key, 3600)
        return BaseResponse({"key": key, "q_token": token}, message="获取七牛上传文件授权成功")
