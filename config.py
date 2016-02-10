# TODO: Add comments to this
DEBUG = True
USE_DEVCONFIG = False

# When debug is enabled, the project will use the devconfig.py file instead (which you need to create)
if DEBUG and USE_DEVCONFIG:
    from devconfig import *
else:
    # Copy everything below this comment into devconfig.py
    # Make sure that you use development keys that are different from your production keys!
    import os

    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'Add Key'

    GOOGLE_API_KEY = 'Add Key'

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = 'Add Key'
    RECAPTCHA_PRIVATE_KEY = 'Add Key'
    RECAPTCHA_PARAMETERS = {}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'example.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'test@example.com'
    MAIL_PASSWORD = 'password'

    sijaxpath = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
    SIJAX_STATIC_PATH = sijaxpath
    SIJAX_JSON_URI = sijaxpath + "json2.js"
