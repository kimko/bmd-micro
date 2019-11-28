# project/api/users.py

from uuid import uuid4

from flask import request
from flask_restful import Resource

# TODO: add model and db support
#  Mocking up users here
ANGELA = {
    "id": 1,
    "lastName": "Merkel",
    "firstName": "Angela",
    "email": "angi@bundestag.de",
    "zipCode": "97202",
}
USERS = [ANGELA]


class UserList(Resource):
    """shows a list of all users, and lets you POST to add a new user
    """

    def get(self):
        response_object = {
            "status": "success",
            "data": {"users": [user for user in USERS]},
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
        # TODO: add model and db support
        USERS.append(
            {
                "id": str(uuid4()),
                "lastName": lastName,
                "firstName": firstName,
                "email": email,
            }
        )
        response_object = {"status": "success", "message": f"{email} was added!"}
        return response_object, 201


class User(Resource):
    """shows a single User and lets you delete and update a User
    """

    def get(self, user_id):
        return {}, 999

    def delete(self, user_id):
        return {}, 999

    def put(self):
        return {}, 999
