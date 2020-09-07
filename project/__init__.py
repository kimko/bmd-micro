# project/__init__.py
"""A flask app with sql extension to be used as a micro serive.
MVP to manage users in a database
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

from redis import from_url as redis_from_url

from project.api.turtle_manager import Turtle_Manager

db = SQLAlchemy()
redis = redis_from_url(os.environ.get("REDIS_URL"))
turtle_manager = Turtle_Manager(redis)


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)
    CORS(app)

    # set config

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    app.config.from_object("project.config_custom.ProductionConfig")
    from logging.config import dictConfig

    dictConfig(app.config["LOGGER"])
    db.init_app(app)

    api = Api(app)

    from project.api.ping import Ping

    api.add_resource(Ping, "/ping")

    from project.api.users import Users, UserList

    api.add_resource(UserList, "/users")
    api.add_resource(Users, "/users/<user_id>")

    from project.api.turtles import TurtlesList
    api.add_resource(TurtlesList, "/turtles")

    # get_count_per_period_and_year
    # example:
    # curl 'localhost:5000/turtlesPeriodYear?period=m'
    from project.api.turtles import TurtlesPeriodYear
    api.add_resource(TurtlesPeriodYear, "/turtlesPeriodYear")

    from project.api.turtles import SumYearSeasonVictory
    api.add_resource(SumYearSeasonVictory, "/sumYearSeasonVictory")

    # example  curl 'localhost:5000/turtlesPeriodStartToEnd?period=m&endDate=2012-12-31'
    from project.api.turtles import TurtlesPeriodStartToEnd
    api.add_resource(TurtlesPeriodStartToEnd, "/turtlesPeriodStartToEnd")

    return app
