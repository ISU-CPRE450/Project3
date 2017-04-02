import json

from flask import request
from flask.views import MethodView

from src.user.user import User


class Users(MethodView):

    def get(self):
        email = request.args.get('email')
        password = request.args.get('password')
        if not all([email, password]):
            return '"email" and "password" required', 400
        user = User.query(User.email == email).get()
        if not user or user.password != password:
            return 'No user exists with those credentials', 404
        return json.dumps(user.serialize()), 200

    def post(self):
        data = request.get_json()
        if not all(
                ['email' in data, 'password' in data, 'account_id' in data]):
            return "'email', 'password', and account_id required", 400
        user = User.query(User.email == data['email']).get()
        if user:
            return 'A user with that email already exists', 409
        user = User.create(data['email'], data['password'], data['account_id'])
        return json.dumps(user.serialize()), 200


def setup_urls(app):
    app.add_url_rule(
        '/user/',
        view_func=Users.as_view('user')
    )
