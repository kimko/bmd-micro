# project/api/models.py


from uuid import uuid4

USERS = {}


class User:
    """I repesent a user with the following arguments:
        id
        lastName
        firstName
        email
        zipcode
    A UUID id will be assigned during initilaztion.
    """

    def __init__(self, email, lastName="", firstName="", zipCode=""):
        """Initialize a user

        Arguments:
            email {str} -- Mandatory argument

        Keyword Arguments:
            lastName {str} -- optional
            firstName {str} -- optional
            zipCode {str} -- optional
        """
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

    def update(id, args):
        user = USERS[id]
        for key, value in args.items():
            setattr(user, key, value)
        return user
