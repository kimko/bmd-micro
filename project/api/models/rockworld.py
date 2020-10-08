# project/api/models.py
"""Represents the data used in the api. Models decouple the application data from application code.

"""
from sqlalchemy.orm import validates

from project import db
from project.api.utils.gravity import Gravity


class RockWorld(db.Model):
    """I repesent a RockWorld in a comma separated string:
        id - mangaged by db
        initialState - text, must be comma sperated with segments of same lenght
        finalState - text, must be comma sperated with segments of same lenght

    Arguments:
        db {SQLAlchemy object} -- Interface to the db
    """

    __tablename__ = "rockworlds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    initialState = db.Column(db.Text(), nullable=False)
    finalState = db.Column(db.Text(), nullable=False)

    def __init__(self, initialState):
        """Initialize a world

        Arguments:
            initialState {str} -- Mandatory argument

        """
        self.initialState = initialState
        self.finalState = Gravity.falling_rocks(initialState)

    @validates("initialState")
    def validates_world(self, key, initialState):
        test_state = initialState.split(",")

        # each row has the same lenght?
        if len(set([len(row) for row in test_state])) != 1:
            raise ValueError("wrong list shape")

        # valid characters?
        valid = " .:T"
        if {char for char in "".join(test_state) if char not in valid}:
            raise ValueError("only ' .:T' allowed")
        return initialState

    def to_json(self):
        """I return all user elements as a key value pair.
        """
        return {
            "id": self.id,
            "initialState": self.initialState.split(","),
            "finalState": self.finalState.split(","),
        }

    def create(self):
        """I wirte a user object to the DB

        Returns:
            RockWorld -- returns the created object
        """
        db.session.add(self)
        db.session.commit()
        return self

    def read(id=""):
        """I read either all or one world from the db

        Keyword Arguments:
            id {integer} -- If supplied, returns one rockworld (default: {""})

        Returns:
            world/s -- either one dictioary or a list of dicts
        """
        if id:
            return RockWorld.query.filter_by(id=int(id)).first()
        else:
            return [world.to_json() for world in RockWorld.query.all()]

    def update(id, data):
        """I update an existing rockworld

        Arguments:
            id {ineger} -- rockworld ID
            args {dictionary} -- Dictionary with rockworld attributes

        Returns:
            [type] -- [description]
        """
        rockworld = RockWorld.query.filter_by(id=int(id)).first()
        if rockworld:
            # the payload + "old" state becomes the new initial state
            # setattr(rockworld, 'initialState', f"{data},{rockworld.finalState}")
            rockworld.initialState = f"{data},{rockworld.finalState}"
            rockworld.finalState = Gravity.falling_rocks(rockworld.initialState)
            db.session.commit()
            return rockworld
        else:
            return False
