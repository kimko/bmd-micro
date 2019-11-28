# project/api/ping.py


from flask_restful import Resource


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "cool"}
