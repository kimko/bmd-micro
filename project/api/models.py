# project/api/models.py
"""Represents the data used in the api. Models decouple the application data from application code.

Returns:
    User -- Describes a User
"""

from project import db


class User(db.Model):
    """I repesent a user with the following arguments:
        id - mangaged by db
        lastName - optional
        firstName - optional
        email - mandatory, must be unqiue
        zipcode - optoinal

    Arguments:
        db {SQLAlchemy object} -- Interface to the db
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
        """I return all user elements as a key value pair.
        """
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "email": self.email,
            "zipCode": self.zipCode,
        }

    def create(self):
        """I wirte a user object to the DB

        Returns:
            User -- returns the created object
        """
        db.session.add(self)
        db.session.commit()
        return self

    def read(id=""):
        """I read either all or one uer from the db

        Keyword Arguments:
            id {integer} -- If supplied, returns one user (default: {""})

        Returns:
            User/s -- one user dictenory or a list of user dicts
        """
        if id:
            return User.query.filter_by(id=int(id)).first()
        else:
            return [user.to_json() for user in User.query.all()]

    def find_by_email(email):
        """ I find one user based on the given email

        Keyword Arguments:
            email {string} -- a email

        Returns:
            User -- one user dictenory or False
        """
        return User.query.filter_by(email=email).first()

    def delete(id):
        """I delete one user based on the given id

        Arguments:
            id {int} -- A user id

        Returns:
            User -- user object or false
        """
        user = User.query.filter_by(id=int(id)).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return user
        else:
            return False

    def update(id, args):
        """I update a user

        Arguments:
            id {ineger} -- User ID
            args {dictionary} -- Dictionary with user attributes

        Returns:
            [type] -- [description]
        """
        user = User.query.filter_by(id=int(id)).first()
        if user:
            for key, value in args.items():
                setattr(user, key, value)
                db.session.commit()
            return user
        else:
            return False
