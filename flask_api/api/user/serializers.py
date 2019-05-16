from flask_restplus import fields
from flask_api.api.restplus import api, base_model

user = api.model("Blog user", {
    "id": fields.Integer(readOnly=True, description="The unique identifier of a blog user"),
    "phone_number": fields.String(required=True, description="phone number"),
    "password": fields.String(required=True, description="password"),
    "nickname": fields.String(required=True, description="nickname"),
    "register_time": fields.DateTime,
})

login_req = api.model("login user", {
    "phone_number": fields.String(required=True, description="phone number"),
    "password": fields.String(required=True, description="password"),
})

token_and_nickname = api.model("token and nickname", {
    "nickname": fields.String(required=True),
    "token": fields.String(required=True),
})

login_resp = api.inherit("login response", base_model, {
    "data": fields.Nested(token_and_nickname)
})

current_user = api.model("current user", {
    "nickname": fields.String(required=True),
    "phone_number": fields.String(required=True, description="phone number"),
})

current_user_resp = api.inherit("current user resp", base_model, {
    "data": fields.Nested(current_user)
})
