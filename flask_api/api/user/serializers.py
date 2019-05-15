from flask_restplus import fields
from flask_api.api.restplus import api

# blog_post = api.model("Blog post", {
#     "id": fields.Integer(readOnly=True, description="The unique identifier of a blog post"),
#     "title": fields.String(required=True, description="Article title"),
#     "body": fields.String(required=True, description="Article content"),
#     "pub_date": fields.DateTime,
#     "category_id": fields.Integer(attribute="category.id"),
#     "category": fields.String(attribute="category.name"),
# })
#
# pagination = api.model("A page of results", {
#     "page": fields.Integer(description="Number of this page of results"),
#     "pages": fields.Integer(description="Total number of pages of results"),
#     "per_page": fields.Integer(description="Number of items per page of results"),
#     "total": fields.Integer(description="Total number of results"),
# })
#
# page_of_blog_posts = api.inherit("Page of blog posts", pagination, {
#     "items": fields.List(fields.Nested(blog_post))
# })
#
# category = api.model("Blog category", {
#     "id": fields.Integer(readOnly=True, description="The unique identifier of a blog category"),
#     "name": fields.String(required=True, description="Category name"),
# })
#
# category_with_posts = api.inherit("Blog category with posts", category, {
#     "posts": fields.List(fields.Nested(blog_post))
# })


# phone_number = db.Column(db.String(11), index=True)
# password = db.Column(db.String(30))
# nickname = db.Column(db.String(30), index=True, nullable=True)
# register_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

user = api.model("Blog user", {
    "id": fields.Integer(readOnly=True, description="The unique identifier of a blog user"),
    "phone_number": fields.String(required=True, description="phone number"),
    "password": fields.String(required=True, description="password"),
    "nickname": fields.String(required=True, description="nickname"),
    "register_time": fields.DateTime,
})

login = api.model("login user", {
    "phone_number": fields.String(required=True, description="phone number"),
    "password": fields.String(required=True, description="password"),
})
