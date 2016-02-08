import flask.ext.login as flask_login
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
mail = Mail(app)

from app import routes, models
