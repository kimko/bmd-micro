# project/api/models.py
"""Represents the data used in the api. Models decouple the application data from application code.

"""

from project import db
from sqlalchemy.orm import validates


def falling_rock(segment):
    """
    orders the list based on "falling_rocks" rules. Super
    slow algorithm comparable to bubble sort.
    """
    for _ in range(len(segment)):
        for i in range(len(segment) - 1):
            if segment[i] == '.' and segment[i + 1] == '.':
                segment[i], segment[i + 1] = ' ', ':'
            if segment[i] == '.' and segment[i + 1] == ' ':
                segment[i], segment[i + 1] = ' ', '.'
            if segment[i] == ':' and segment[i + 1] == ' ':
                segment[i], segment[i + 1] = ' ', ':'
            if segment[i] == ':' and segment[i + 1] == '.':
                segment[i], segment[i + 1] = '.', ':'
    return segment


def transpose_list(lists):
    """
    transposes a 2d array
    """
    return [list(x) for x in zip(*lists)]


def falling_rocks(initialState):
    print("INITIAL STATE")  # TODO remove print
    print(initialState)  # TODO remove print
    # convert string into list of strings
    fState = initialState.split(',')
    # transpose list of strings into segments
    fState = transpose_list(fState)
    # simulate "falling rock" in each segment
    fState = [falling_rock(segment) for segment in fState]
    # transpose back into original format
    fState = [list(left) for left in zip(*fState)]
    # remove empty rows
    fState_copy = fState
    for row, _ in enumerate(fState_copy):
        if set(fState[row]) == ({' '}):
            del fState[row]
    # return as string
    print("FINAL STATE")  # TODO remove print
    print(",".join([''.join(row) for row in fState]))
    return ",".join([''.join(row) for row in fState])


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
        self.finalState = falling_rocks(initialState)

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
        print("MODEL")
        print(self.initialState)
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
            print(RockWorld.query.filter_by(id=int(id)).first().initialState)
            return RockWorld.query.filter_by(id=int(id)).first()
        else:
            return [world.to_json() for world in RockWorld.query.all()]
