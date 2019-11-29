# project/api/ping.py


from flask_restful import Resource

from project.api.metrics import timing


class Ping(Resource):
    @timing
    def get(self):
        return {"status": "success", "message": "cool"}
