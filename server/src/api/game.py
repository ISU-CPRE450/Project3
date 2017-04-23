from datetime import datetime, timedelta
import json

from flask import request
from flask.views import MethodView

from src.game.game import Game
from src.user.user import User


class LatestGame(MethodView):

    def get(self):
        game = Game.query(Game.is_active == False).order(
            -Game.time_created).get()
        if not game:
            return 'No games exist in database', 400
        return json.dumps(game.serialize()), 200


class GameHistory(MethodView):

    def get(self):
        yesterday = datetime.now() - timedelta(days=1)
        games = Game.query(
            Game.is_active == False, Game.time_created > yesterday).order(
                -Game.time_created).fetch()
        games = [g.serialize() for g in games]
        return json.dumps(games), 200


class BankerGameAPI(MethodView):

    def get(self, game_id):
        game = Game.get_by_id(game_id)
        if not game:
            return 'Game not found', 400
        return json.dumps(game.serialize()), 200

    def post(self, banker_id):
        banker = User.query(User.account_id == banker_id).get()
        if not banker:
            return 'Banker not found', 400
        if Game.banker_already_proctoring(banker):
            return 'This banker is already proctoring another game', 400
        g = Game.add(banker)
        return json.dumps(g.serialize()), 200

    def delete(self, game_id):
        g = Game.get_by_id(game_id)
        if not g:
            return 'Could not find game', 202
        g.end()
        return 'Success', 200


class ParticipantGameAPI(MethodView):

    def post(self, participant_id):
        user = User.query(User.account_id == participant_id).get()
        if not user:
            return 'User does not exist in system', 400
        game = Game.get_available_game()
        if not game:
            return 'There are no games available to join, please try again '\
                   'later', 400
        data = request.get_json()
        if 'amount' not in data or 'hash_value' not in data or \
                'random_value' not in data:
            return '"amount" and "hash_value" required', 400
        try:
            amount = float(data['amount'])
        except:
            return 'amount must be float', 400
        try:
            random_value = int(data['random_value'])
        except:
            return 'random_value must be int', 400
        p = user.spawn_participant(amount, random_value, data['hash_value'])
        try:
            game.add_participant(p)
        except Exception as e:
            return e.message, 400
        return json.dumps(game.serialize()), 200


def setup_urls(app):
    # BANKER
    app.add_url_rule(
        '/api/game/<banker_id>/', methods=['POST'],
        view_func=BankerGameAPI.as_view('game.new'))
    app.add_url_rule(
        '/api/game/<int:game_id>/', methods=['GET', 'DELETE'],
        view_func=BankerGameAPI.as_view('game'))

    # PARTICIPANT
    app.add_url_rule(
        '/api/game/join/<participant_id>/',
        view_func=ParticipantGameAPI.as_view('game.join'))

    # GAME
    app.add_url_rule(
        '/api/game/latest/',
        view_func=LatestGame.as_view('game.latest'))
    app.add_url_rule(
        '/api/game/history/',
        view_func=GameHistory.as_view('game.history'))
