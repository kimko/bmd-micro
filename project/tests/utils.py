# project/tests/utils.py


from project.api.models import User


def add_user(email="", lastName="", firstName="", zipCode=""):
    user = User(email, lastName, firstName, zipCode).create()
    return user
