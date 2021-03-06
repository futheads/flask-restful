from flask_restplus import fields
from flask_api.api.restplus import api

user_model = api.model("user", {
    "id": fields.Integer(readOnly=True, description="The unique identifier of a blog user"),
    "phone_number": fields.String(required=True, description="phone number"),
    "password": fields.String(required=True, description="password"),
    "nickname": fields.String(required=True, description="nickname"),
    "register_time": fields.DateTime,
})
