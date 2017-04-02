import requests
import json

from stellar_base.keypair import Keypair

from src.user import User

SERVER_URL = "http://localhost:9088"


class UserFactory(object):

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def print_title(self):
        raise NotImplementedError

    def get_or_create_user(self):
        raise NotImplementedError

    def _verify_credentials_set(self):
        if not self.email or not self.password:
            raise Exception('Email or password not set')

    def _jsonify(self):
        return json.dumps(self._serialize())

    def _serialize(self):
        return {
            'email': self.email,
            'password': self.password
        }

    def _headers(self):
        return {
            'Content-Type': 'application/json'
        }


class LoginFactory(UserFactory):

    def print_title(self):
        print "=" * 10 + " Log in " + "=" * 10

    def get_or_create_user(self):
        url = '%s/user/' % SERVER_URL
        r = requests.get(url, params=self._serialize())
        if not r.ok:
            raise Exception(r.content)
        print "Successfully logged in!"
        return User(**r.json())


class NewAccountFactory(UserFactory):

    def print_title(self):
        print "=" * 10 + " New Account " + "=" * 10

    def get_or_create_user(self):
        url = '%s/user/' % SERVER_URL
        data = self._serialize()
        data['account_id'] = self._generate_public_key()
        r = requests.post(url, headers=self._headers(), data=json.dumps(data))
        if not r.ok:
            raise Exception(r.content)
        print "New user successfully created!"
        return User(**r.json())

    def _generate_public_key(self):
        kp = Keypair.random()
        return kp.address().decode()
