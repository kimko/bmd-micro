# project/tests/utils.py
"""testing utilities
"""

from project.api.models.user import User


def add_user(email="", lastName="", firstName="", zipCode=""):
    user = User(email, lastName, firstName, zipCode).create()
    return user
