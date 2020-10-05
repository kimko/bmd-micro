# project/api/models.py
"""Represents the data used in the api. Models decouple the application data from application code.

"""

from project import db
from sqlalchemy.orm import validates


class RockWorld(db.Model):
    """I repesent a RockWorld in a comma separated string:
        id - mangaged by db
        world - text, must be comma sperated with segments of same lenght

    Arguments:
        db {SQLAlchemy object} -- Interface to the db
    """

    __tablename__ = "rockworlds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    world = db.Column(db.Text(), nullable=False)

    def __init__(self, world):
        """Initialize a world

        Arguments:
            world {str} -- Mandatory argument

        """
        self.world = world

    @validates("world")
    def validates_world(self, key, world):
        test_world = world.split(",")

        # each row has the same lenght?
        if len(set([len(row) for row in test_world])) != 1:
            raise ValueError("wrong list shape")

        # valid characters?
        valid = " .:T"
        if {char for char in "".join(test_world) if char not in valid}:
            raise ValueError("only ' .:T' allowed")
        return world

    def to_json(self):
        """I return all user elements as a key value pair.
        """
        return {"id": self.id, "world": self.world.split(",")}

    def create(self):
        """I wirte a user object to the DB

        Returns:
            RockWorld -- returns the created object
        """
        print("MODEL")
        print(self.world)
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
            print("READ")
            print(RockWorld.query.filter_by(id=int(id)).first().world)
            return RockWorld.query.filter_by(id=int(id)).first()
        else:
            return [world.to_json() for world in RockWorld.query.all()]
