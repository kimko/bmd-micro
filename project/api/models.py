# project/api/models.py


from uuid import uuid4

USERS = {}


class User:
    def __init__(self, email, lastName="", firstName="", zipCode=""):
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
        USERS[self.id] = self
        return self

    def read(id=""):
        if id:
            return USERS[id]
        else:
            return [user.to_json() for key, user in USERS.items()]

    def find(email):
        for key, user in USERS.items():
            if user.email == email:
                return user

    def delete(id):
        return USERS.pop(id)
