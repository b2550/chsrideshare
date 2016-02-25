import flask.ext.login as flask_login
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
try:
    app.config.from_object('config')
except AttributeError:
    app.logger.warning(
        'Enviroment config failed, trying \'noconfig.py\' file. If this fails then the fallback config does not exist.')
    app.config.from_object('noconfig')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
mail = Mail(app)

from app import routes, models
