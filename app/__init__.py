import flask.ext.login as flask_login
import flask_sijax
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy

# TODO: Add print() debug

app = Flask(__name__)
try:
    app.config.from_object('config')
    if app.config.get('BADCONFIG'):
        app.logger.critical('!!!   APP NOT CONFIGURED  !!!')
        app.logger.error('!!!        CRASHING       !!!')
        raise RuntimeError('Environment Configuration Failed: Please Check')
except:
    app.config.from_object('config_fallback')
    app.logger.critical('!!!   APP CONFIGURED INCORRECTLY  !!!')
    app.logger.critical('!!!     USING FALLBACK CONFIG     !!!')
    app.logger.critical('!!!       ERRORS WILL OCCUR       !!!')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
mail = Mail(app)
flask_sijax.Sijax(app)

from app import routes, models
