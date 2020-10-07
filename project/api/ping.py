# project/api/ping.py
"""All routes pertaining to the Ping object are manged here.
The flask-restful resources will be mapped to a route in project.__init__.
All user interactions will be logged in a structured way (time stamp, module, message)
"""
from flask_restful import Resource

from project.api.utils.metrics import timing


class Ping(Resource):
    """I provide simple healthcheck functionality
    """

    @timing
    def get(self):
        """get route - will provide simple status and message when called.
        """
        return {"status": "success", "message": "cool"}
