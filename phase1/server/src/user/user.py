import requests

from google.appengine.ext import ndb


class User(ndb.Model):
    account_id = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    secret = ndb.StringProperty(required=True)

    @classmethod
    def create(cls, email, password, account_id, secret):
        cls._create_in_stellar(account_id)
        user = User(
            email=email,
            password=password,
            account_id=account_id,
            secret=secret
        )
        user.put()
        return user

    @classmethod
    def _create_in_stellar(cls, account_id):
        url = 'https://horizon-testnet.stellar.org/friendbot?addr=%s' % \
            account_id
        r = requests.get(url)
        r.raise_for_status()

    def serialize(self):
        return self._to_dict()
