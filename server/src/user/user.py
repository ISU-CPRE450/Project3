from google.appengine.ext import ndb


class User(ndb.Model):
    account_id = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)

    @classmethod
    def create(cls, email, password, account_id):
        user = User(
            email=email,
            password=password,
            account_id=account_id
        )
        user.put()
        return user

    def serialize(self):
        return self._to_dict()
