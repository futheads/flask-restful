from flask_restplus import fields
from flask_api.api.restplus import api, base_model

phone_number_field = api.model("phone number", {
    "phone_number": fields.String(required=True, description="phone number"),
})

sm_validate_req = api.inherit("short message validate_req", phone_number_field, {
    "validate_number": fields.String(required=True, description="validate_number"),
})

login_req = api.inherit("login user", phone_number_field, {
    "password": fields.String(required=True, description="password"),
})

token_and_nickname = api.model("token and nickname", {
    "nickname": fields.String(required=True),
    "token": fields.String(required=True),
})

login_resp = api.inherit("login response", base_model, {
    "data": fields.Nested(token_and_nickname)
})

current_user = api.inherit("current user", phone_number_field, {
    "nickname": fields.String(required=True),
})

current_user_resp = api.inherit("current user resp", base_model, {
    "data": fields.Nested(current_user)
})

qiniu_token = api.model("qiniu token", {
    "key": fields.String(required=True),
    "q_token": fields.String(required=True)
})

qiniu_token_resp = api.inherit("qiniu token rsp", base_model, {
    "data": fields.Nested(qiniu_token)
})
