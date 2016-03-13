import flask.ext.login as flask_login
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.bower import Bower
from flask.ext.mail import Mail
from flask.ext.scss import Scss
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')

app.logger.info('If app fails then check env configuration')
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
mail = Mail(app)
Scss(app)
Bower(app)
app.config['BOWER_URL_PREFIX'] = '/'

app.logger.info('App initialized')

from app import routes, models
