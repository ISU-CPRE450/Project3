from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from src.api.game import setup_urls as setup_game_urls
from src.api.user import setup_urls as setup_user_urls

APP_DEBUG = True

app = Flask(__name__)
app.debug = APP_DEBUG
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = 'Secret_Coin_Flipper_Key'
# app.url_map.converters['regex'] = RegexConverter
toolbar = DebugToolbarExtension(app)

setup_game_urls(app)
setup_user_urls(app)


@app.errorhandler(500)
def handle_bad_request(e):
    exp_type = type(e).__name__ or "Unknown"
    m = "The server hit an unhandled exception!<br>" \
        "Exception Type: %s<br>" \
        "Exception Message: %s" % (exp_type, e.message)
    return m, 500
