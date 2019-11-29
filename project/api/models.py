# project/api/models.py


from uuid import uuid4

USERS = []


class User():

    def __init__(self, lastName, firstName, email, zipCode):
        self.id = str(uuid4())
        self.lastName = lastName
        self.firstName = firstName
        self.email = email
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
        USERS.append(self.to_json())

    def read(id=""):
        if not id:
            return [user for user in USERS]
