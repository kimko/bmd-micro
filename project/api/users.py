# project/api/users.py

from flask import current_app as app
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
            "message": "Get all users",
        }
        app.logger.info(response_object["message"])
        return response_object, 200

    def post(self):
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            app.logger.info(response_object["message"])
            return response_object, 400
        try:
            email = post_data["email"]
            if not User.find(email):
                User(**post_data).create()
                response_object = {
                    "status": "success",
                    "message": f"{email} was added!",
                }
                app.logger.info(response_object["message"])
                return response_object, 201
            else:
                response_object[
                    "message"
                ] = "User with email {} already exists.".format(email)
                app.logger.info(response_object["message"])
                return response_object, 400
        except KeyError:
            app.logger.info(response_object["message"])
            return response_object, 400


class Users(Resource):
    """shows a single User and lets you delete and update a User
    """

    def get(self, user_id):
        response_object = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.read(user_id)
            response_object = {
                "status": "success",
                "data": user.to_json(),
                "message": "Get user",
            }
            app.logger.info(response_object["message"])
            return response_object, 200
        except KeyError:
            app.logger.info(response_object["message"])
            return response_object, 404

    def delete(self, user_id):
        return {}, 999

    def put(self):
        return {}, 999
