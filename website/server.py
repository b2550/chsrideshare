import sqlite3
from contextlib import closing

import flask.ext.login as flask_login
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask.ext.bcrypt import Bcrypt
from flask_login import login_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

# <editor-fold desc="Config and Init">
# TODO: add more config
DATABASE = 'database.db'
DEBUG = True
# TODO: Remember to change this!
SECRET_KEY = 'SQIZ9zxyckj4h-9=ssdu&s!y42s7%bv#k+d(!n8u(s&1ifi)fo2degIT'
SCHEMA = 'schema.sql'

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.config.from_object(__name__)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# </editor-fold>


# TODO: Add more syntax comments


# <editor-fold desc="Database Methods">
def connect_db():
    """Connects to database from config"""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Initializes database with schema.sql file"""
    with closing(connect_db()) as db:
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Gets the currently connected database (which in this case is only the one application database)"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Closes the connection to the database when app process is terminated"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """
    Query's the database with SQL command and variable inputs
    Args:
        query: SQL query
        args: Comma separated values that replace all question marks in the SQL query respectively
        one: When true, returns one item from the query
    Returns:
        SQL query values in list[tuple] type
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# </editor-fold>


# <editor-fold desc="Forms">
# TODO: add bcrypt to validation
# <editor-fold desc="Form Validation">
def login_validate(form, field):
    """Validates the login form"""
    fpass = form["password"]
    dbuser = query_db('SELECT username FROM users WHERE username = ?', (field.data,), one=True)
    dbpass = query_db('SELECT password FROM users WHERE username = ?',
                      [field.data], one=True)
    if dbuser is None:
        raise ValidationError("Check that you entered everything correctly")
    elif bcrypt.check_password_hash(dbpass[0], fpass.data) is False:
        raise ValidationError("Check that you entered everything correctly")


def register_validate(form, field):
    """Validates the register form"""
    femail = form["email"]
    dbuser = query_db('SELECT username FROM users WHERE username = ?', (field.data,), one=True)
    dbpass = query_db('SELECT password FROM users WHERE password = ?', (femail.data,), one=True)
    if dbuser is not None:
        raise ValidationError("Someone stole your username! Guess you have to pick a different one.")
    elif dbpass is not None:
        raise ValidationError("Email already in use. If you forget your username or password you can reset that from"
                              " the login page.")


# </editor-fold>


# <editor-fold desc="Form Builders">
class LoginForm(Form):
    """Creates a login form when called"""
    username = StringField('Username', validators=[DataRequired(message="You forgot to enter a username! You ok?"),
                                                   login_validate])
    password = PasswordField('Password', validators=[DataRequired(message="You forgot to enter a password! You ok?")])
    remember = BooleanField('Remember <e')


# TODO: ADD RECAPCHA
class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired(
            message='You need a username silly, or you wont be able to login'), register_validate])
    password = PasswordField('Password', validators=[DataRequired(
            message='You need a password silly, or else people can just login as you by knowing your username')])
    passwordvalidate = PasswordField('Repeat Password', validators=[DataRequired(
            message='You need to fill this out! We just need to check that you didn\'t mess up your password'
                    ' by accident.'), EqualTo('password', message='Oh jeez, looks like you mistyped your password.'
                                                                  ' Do me a big favor and type it in to both password'
                                                                  ' boxes again so I don\'t have to reset it for you'
                                                                  ' later.')])
    email = StringField('Email', validators=[DataRequired(message='You need an email so we can contact you and give'
                                                                  ' you notifications. Don\'t worry, we won\'t spam you'
                                                                  ' or give your email away to anyone'),
                                             Email(message='Whoops, looks like you forgot to put an @ sign or maybe a'
                                                           ' .com? Just check to see if you typed that in right.')])
    type = SelectField('type', choices=[('admin', 'Admin'), ('student', 'Student'), ('parent', 'Parent')])


# </editor-fold>
# </editor-fold>


# <editor-fold desc="Routes">
# TODO: update all dis to be more api-style
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('User validated with database! Yay!')
            login_user(form.username.data, remember=form.remember.data)
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


# TODO: CREATE LOGOUT SYSTEM
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# TODO: DEBUG: REMOVE THIS: ADD FIRST RUN OVERRIDE FOR LOGIN PAGE TO CREATE ADMIN ACCOUNT

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = bcrypt.generate_password_hash(form.password.data)
            email = form.email.data
            utype = form.type.data
            g.db.execute('INSERT INTO users (username, password, email, type) VALUES (?, ?, ?, ?)',
                         [username, password, email, utype])
            g.db.commit()
            flash('Registered the user ' + username)
            return render_template('register.html', form=form)
        else:
            flash('did not validate')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


# TODO: DEBUG: REMOVE THIS: MAKE USER MANAGER FOR ADMIN


@app.route('/listusers')
def listusers():
    db = get_db()
    cur = db.execute('SELECT username, password FROM users ORDER BY id DESC')
    entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    return render_template('makeadmin.html', entries=entries)


@app.route('/initdb')
def do_init_db():
    init_db()
    return redirect('/listusers')

# </editor-fold>


if __name__ == '__main__':
    app.run(None, 8001)
