# project/__init__.py

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


db = SQLAlchemy()


def create_app(script_info=None):
    from project.config import LoggerConfig

    LoggerConfig()

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    api = Api(app)

    from project.api.ping import Ping

    api.add_resource(Ping, "/ping")

    from project.api.users import Users, UserList

    api.add_resource(UserList, "/users")
    api.add_resource(Users, "/users/<user_id>")

    return app
