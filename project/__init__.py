# project/__init__.py
"""A flask app with sql extension to be used as a micro serive.
MVP to manage users in a database
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


db = SQLAlchemy()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

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

    return app
