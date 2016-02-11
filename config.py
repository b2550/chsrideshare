import os

DEBUG = os.environ('APP_DEBUG')
TESTING = os.environ('APP_TESTING')

BADCONFIG = os.environ('APP_BADCONFIG')

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ('APP_SECRET_KEY')

GOOGLE_API_KEY = os.environ('APP_GOOGLE_API_KEY')

RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = os.environ('APP_RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ('APP_RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PARAMETERS = {}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIL_SERVER = os.environ('APP_MAIL_SERVER')
MAIL_PORT = os.environ('APP_MAIL_PORT', 465)
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ('APP_MAIL_USERNAME')
MAIL_PASSWORD = os.environ('APP_MAIL_PASSWORD')

sijaxpath = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
SIJAX_STATIC_PATH = sijaxpath
SIJAX_JSON_URI = sijaxpath + "json2.js"