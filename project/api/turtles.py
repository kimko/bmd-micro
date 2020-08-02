import json

from flask import current_app as app
from flask_restful import Resource

from project.api.metrics import timing

from project import redis

from project.api.turtle_manager import Turtle_Manager


ALL_TURTLES = 'all_turtles'


class TurtlesList(Resource):

    @timing
    def get(self):
        """
        Get all Turtles
        """

        if not redis.exists(ALL_TURTLES):
            app.logger.info("Loading Turtles from S3")
            manager = Turtle_Manager()
            response_object = {
                "status": "success",
                "data": {"turtles": manager.get_df().to_json()},
                "message": "Get all turtles",
            }
            app.logger.info(response_object["message"])
            redis.set(ALL_TURTLES, json.dumps(response_object))
        else:
            app.logger.info("Loading Turtles from Redis")
            response_object = json.loads(redis.get(ALL_TURTLES))
            # redis.delete(ALL_TURTLES)

        return response_object, 200


if __name__ == '__main__':
    # for local testing
    df = Turtle_Manager().get_df()
