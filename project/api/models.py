# project/api/models.py


from uuid import uuid4

USERS = []


class User():

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
        USERS.append(self)
        return self

    def read(id=""):
        if id:
            for user in USERS:
                if user.id == id:
                    return user
        else:
            return [user.to_json() for user in USERS]

    def find(email):
        for user in USERS:
            if user.email == email:
                return user
