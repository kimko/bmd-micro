# project/api/users.py
"""All routes pertaining to the user object are manged here.
The flask-restful resources will be mapped to a route in project.__init__.
All user interactions will be logged in a structured way (time stamp, module, message)

Execution of each route will be timed and logged.
    IE - Updating a user object with aput request:
    [2019-11-29 23:43:48,060] in users: 864acfcc-ae05-4485-80c9-1066bc761c11 was updated!
    [2019-11-29 23:43:48,062] in metrics: Users.put() 1.67ms
"""
import json

from flask import current_app as app
from flask import request
from flask_restful import Resource

from project.api.metrics import timing
from project.api.models import User

from project import redis


class UserList(Resource):
    """shows a list of all users, and lets you POST to add a new user. Implemented routes:
        get: returns all users
        post(payload): creates a new user (if email does not exist yet)
    """
    path = 'AllUsers'

    @timing
    def get(self):
        if not redis.exists(self.path):
            app.logger.info("get UserList here")
            response_object = {
                "status": "success",
                "data": {"users": User.read()},
                "message": "Get all users",
            }
            app.logger.info(response_object["message"])
            redis.set(self.path, json.dumps(response_object))
        else:
            app.logger.info("read UserList from Redis")
            response_object = json.loads(redis.get(self.path))

        return response_object, 200

    @timing
    def post(self):
        redis.delete(self.path)
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            app.logger.info(response_object["message"])
            return response_object, 400
        try:
            email = post_data["email"]
            if not User.find_by_email(email):
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
    """manages single users. Implemented routes:
        get(id): returns a user
        delete(id): deletes a user
        put(id, payload): updates a user
    """

    @timing
    def get(self, user_id):
        app.logger.info("get user here")
        response_object = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.read(user_id)
            if user:
                response_object = {
                    "status": "success",
                    "data": user.to_json(),
                    "message": "Get user",
                }
                app.logger.info(response_object["message"])
                return response_object, 200
            else:
                app.logger.info(response_object["message"])
                return response_object, 404
        except ValueError:
            app.logger.info(response_object["message"])
            return response_object, 404

    @timing
    def delete(self, user_id):
        redis.delete('AllUsers')
        response_object = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.delete(user_id)
            if user:
                response_object["status"] = "success"
                response_object["message"] = f"{user.email} was removed!"
                app.logger.info(response_object["message"])
                return response_object, 200
            else:
                app.logger.info(response_object["message"])
                return response_object, 404
        except ValueError:
            response_object["message"] = "Invalid payload."
            return response_object, 404

    @timing
    def put(self, user_id):
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            app.logger.info(response_object["message"])
            return response_object, 400
        try:
            user = User.update(user_id, post_data)
            if user:
                response_object["status"] = "success"
                response_object["message"] = f"{user.id} was updated!"
                app.logger.info(response_object["message"])
                return response_object, 200
            else:
                response_object = {"status": "fail", "message": "User does not exist"}
                app.logger.info(response_object["message"])
                return response_object, 404
        except ValueError:
            return response_object, 404
