from flask import current_app as app
from flask import request
from flask_restful import Resource

from project.api.utils.metrics import timing
from project.api.models.rockworld import RockWorld


class RockWorldsList(Resource):
    """shows a list of all rockworlds, and lets you POST to add a new user. Implemented routes:
        get: returns all rockworlds
        post(payload): creates a new RockWorld (if email does not exist yet)
    """

    @timing
    def get(self):
        response_object = {
            "status": "success",
            "data": RockWorld.read(),
            "message": "Get all rockworlds",
        }
        app.logger.info(response_object["message"])
        return response_object, 200

    @timing
    def post(self):
        response_object = {"status": "fail", "message": "Invalid payload."}
        try:
            post_data = request.get_json()
            if type(post_data) is not list:
                response_object["message"] += f" ValueError: list expected"
                app.logger.info(response_object["message"])
                return response_object, 400
        except AttributeError:
            # TODO TEST missing
            response_object["message"] += " Json List Object expected."
            app.logger.info(response_object["message"])
            return response_object, 400

        try:
            rockworld = RockWorld(initialState=",".join(post_data)).create()
            response_object = {
                "status": "success",
                "message": f"World {rockworld.id} was added!",
                # "data": [rockworld.world.split(",")],
                "data": [rockworld.to_json()],
            }
            app.logger.info(response_object["message"])
            return response_object, 201
        except KeyError as err:
            # TODO TEST missing
            response_object["message"] += f" KeyError: {str(err)}"
            app.logger.info(response_object["message"])
            return response_object, 400
        except TypeError as err:
            # TODO TEST missing
            response_object["message"] += f" TypeError: {str(err)}"
            app.logger.info(response_object["message"])
            return response_object, 400
        except ValueError as err:
            response_object["message"] += f" ValueError: {str(err)}"
            app.logger.info(response_object["message"])
            return response_object, 400


class RockWorlds(Resource):
    """manages single rockworlds. Implemented routes:
        get(id): returns a rockworld
        delete(id): deletes a rockworld
        put(id, payload): updates a rockworld
    """

    @timing
    def get(self, world_id):
        response_object = {"status": "fail", "message": "rockworld does not exist"}
        try:
            rockworld = RockWorld.read(world_id)
            if rockworld:
                print("API")
                print(rockworld.initialState)
                response_object = {
                    "status": "success",
                    "data": [rockworld.to_json()],
                    "message": "Get rockworld",
                }
                app.logger.info(response_object["message"])
                return response_object, 200
            else:
                # TODO test missing
                app.logger.info(response_object["message"])
                return response_object, 404
        except ValueError:
            # TODO test missing
            app.logger.info(response_object["message"])
            return response_object, 404
