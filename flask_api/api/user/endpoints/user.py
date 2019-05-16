import logging

from flask import request
from flask_restplus import Resource
from flask_api.api.user.business import create_user, update_user, delete_user
from flask_api.api.user.serializers import user

from flask_api.api.restplus import api, login_check
from flask_api.database.models import User


log = logging.getLogger(__name__)

ns = api.namespace("users", description="Operations related to users")


@ns.route("/")
class UserCollection(Resource):

    @login_check
    @api.marshal_list_with(user)
    def get(self):
        """
        Returns list of users.
        """
        categories = User.query.all()
        return categories

    @api.doc(security=None)
    @api.response(201, "User successfully created.")
    @api.expect(user)
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json
        create_user(data)
        return None, 201


@ns.route("/<int:id>")
@api.response(404, "User not found.")
class UserItem(Resource):

    @login_check
    @api.marshal_with(user)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return User.query.filter(User.id == id).one()

    @login_check
    @api.expect(user)
    @api.response(204, "Category successfully updated.")
    def put(self, id):
        """
        Updates a user
        """
        data = request.json
        update_user(id, data)
        return None, 204

    @login_check
    @api.response(204, "Category successfully deleted.")
    def delete(self, id):
        """
        Deletes user.
        """
        delete_user(id)
        return None, 204


