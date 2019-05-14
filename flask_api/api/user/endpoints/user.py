import logging

from flask import request
from flask_restplus import Resource
from flask_api.api.blog.business import create_category, delete_category, update_category
from flask_api.api.user.serializers import user

from flask_api.api.restplus import api
from flask_api.database.models import User

log = logging.getLogger(__name__)

ns = api.namespace("users", description="Operations related to users")


@ns.route("/")
class UserCollection(Resource):

    @api.header('X-Header', 'Some class header')
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
        create_category(data)
        return None, 201


@ns.route("/<int:id>")
@api.response(404, "User not found.")
class UserItem(Resource):

    @api.marshal_with(user)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return User.query.filter(User.id == id).one()

    @api.expect(user)
    @api.response(204, "Category successfully updated.")
    def put(self, id):
        """
        Updates a blog category.

        Use this method to change the name of a blog category.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "name": "New Category Name"
        }
        ```

        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        update_category(id, data)
        return None, 204

    @api.response(204, "Category successfully deleted.")
    def delete(self, id):
        """
        Deletes blog category.
        """
        delete_category(id)
        return None, 204
