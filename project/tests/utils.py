# project/tests/utils.py
"""testing utilities
"""
from project.api.models.rockworld import RockWorld
from project.api.models.user import User


def add_user(email="", lastName="", firstName="", zipCode=""):
    user = User(email, lastName, firstName, zipCode).create()
    return user


def add_rockworld(world):
    world = RockWorld(world).create()
    return world
