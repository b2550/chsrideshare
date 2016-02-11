import os

DEBUG = False
TESTING = False

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.urandom(32)

GOOGLE_API_KEY = None

RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = None
RECAPTCHA_PRIVATE_KEY = None
RECAPTCHA_PARAMETERS = {}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIL_SERVER = None
MAIL_PORT = None
MAIL_USE_SSL = True
MAIL_USERNAME = None
MAIL_PASSWORD = None

sijaxpath = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
SIJAX_STATIC_PATH = sijaxpath
SIJAX_JSON_URI = sijaxpath + "json2.js"
