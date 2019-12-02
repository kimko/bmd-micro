# project/api/models.py


import os
from uuid import uuid4

from sqlalchemy.sql import func

from project import db


USERS = {}


class User(db.Model):
    """I repesent a user with the following arguments:
        id
        lastName
        firstName
        email
        zipcode
    A UUID id will be assigned during initilaztion.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False)
    lastName = db.Column(db.String(128), nullable=True)
    firstName = db.Column(db.String(128), nullable=True)
    zipCode = db.Column(db.String(5), nullable=True)

    def __init__(self, email, lastName="", firstName="", zipCode=""):
        """Initialize a user

        Arguments:
            email {str} -- Mandatory argument

        Keyword Arguments:
            lastName {str} -- optional
            firstName {str} -- optional
            zipCode {str} -- optional
        """
        self.email = email
        self.lastName = lastName
        self.firstName = firstName
        self.zipCode = zipCode

    def to_json(self):
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "email": self.email,
            "zipCode": self.zipCode,
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(id=""):
        if id:
            return User.query.filter_by(id=int(id)).first()
        else:
            return [user.to_json() for user in User.query.all()]

    def find(email):
        for key, user in USERS.items():
            if user.email == email:
                return user

    def delete(id):
        return USERS.pop(id)

    def update(id, args):
        user = USERS[id]
        for key, value in args.items():
            setattr(user, key, value)
        return user
