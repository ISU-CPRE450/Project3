import json

from flask.views import MethodView

from src.game.game import Game
from src.user.user import User


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


def setup_urls(app):
    app.add_url_rule(
        '/api/game/<banker_id>/', methods=['POST'],
        view_func=BankerGameAPI.as_view('game.new'))

    app.add_url_rule(
        '/api/game/<int:game_id>/', methods=['GET', 'DELETE'],
        view_func=BankerGameAPI.as_view('game'))
