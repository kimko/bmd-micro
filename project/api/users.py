# project/api/users.py

from flask import request
from flask_restful import Resource

from project.api.models import User


class UserList(Resource):
    """shows a list of all users, and lets you POST to add a new user
    """

    def get(self):
        response_object = {
            "status": "success",
            "data": {"users": User.read()},
        }
        return response_object, 200

    def post(self):
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            return response_object, 400
        lastName = post_data.get("lastName")
        firstName = post_data.get("firstName")
        email = post_data.get("email")
        zipCode = post_data.get("zipCode")
        User(lastName, firstName, email, zipCode).create()
        response_object = {"status": "success", "message": f"{email} was added!"}
        return response_object, 201


class Users(Resource):
    """shows a single User and lets you delete and update a User
    """

    def get(self, user_id):
        return {}, 999

    def delete(self, user_id):
        return {}, 999

    def put(self):
        return {}, 999
