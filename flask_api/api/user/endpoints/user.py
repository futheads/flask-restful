import logging

from flask import request, g
from flask_restplus import Resource
from flask_api.api.user.business import create_user, update_user, delete_user
from flask_api.api.user.serializers import user_model

from flask_api.api.restplus import api, login_check, log_record
from flask_api.database.models import User


log = logging.getLogger(__name__)

ns = api.namespace("users", description="Operations related to users")


@ns.route("/")
class UserCollection(Resource):

    @log_record
    @login_check
    @api.marshal_list_with(user_model)
    def get(self):
        """
        Returns list of users.
        """
        categories = User.query.all()
        return categories

    @api.doc(security=None)
    @api.response(201, "User successfully created.")
    @api.expect(user_model)
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json
        # phone_number = data.get("phone_number")
        # is_validate = redis_store.get("is_validate:%s" % phone_number)
        # if is_validate != "1":
        #     raise ValidationError("is_validate", message="验证码没有通过")
        create_user(data)
        # redis_store.delete("is_validate:%s" % phone_number)
        # redis_store.delete("register:%s" % phone_number)
        return None, 201


@ns.route("/<int:id>")
@api.response(404, "User not found.")
class UserItem(Resource):

    @log_record
    @login_check
    @api.marshal_with(user_model)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return User.query.filter(User.id == id).one()

    @log_record
    @login_check
    @api.expect(user_model)
    @api.response(204, "Category successfully updated.")
    def put(self, id):
        """
        Updates a user
        """
        data = request.json
        update_user(id, data)
        return None, 204

    @log_record
    @login_check
    @api.response(204, "Category successfully deleted.")
    def delete(self, id):
        """
        Deletes user.
        """
        delete_user(id)
        return None, 204
