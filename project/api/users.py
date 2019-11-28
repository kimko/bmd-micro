# project/api/users.py

from flask_restful import Api, Resource


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
        return {}, 999


class User(Resource):
    """shows a single User and lets you delete and update a User
    """

    def get(self, user_id):
        return {}, 999

    def delete(self, user_id):
        return {}, 999

    def put(self):
        return {}, 999
