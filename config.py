import os

basedir = os.path.abspath(os.path.dirname(__file__))

# TODO: add more config
DEBUG = True
# TODO: Remember to change this!
SECRET_KEY = 'SQIZ9zxyckj4h-9=ssdu&s!y42s7%bv#k+d(!n8u(s&1ifi)fo2degIT'

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6Ldz2hYTAAAAAG4yR3cABwtC-qo8SO5pWcgVA_i5'
RECAPTCHA_PRIVATE_KEY = '6Ldz2hYTAAAAAFGU5JEz_sxrWCmlq7S_TzytdJ-8'
RECAPTCHA_PARAMETERS = {}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
