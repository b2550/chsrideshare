import flask.ext.login as flask_login
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask.ext.bcrypt import Bcrypt
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError

# Default Config
DATABASE = 'squizit.db'
DEBUG = True
SECRET_KEY = 'SQIZ9zxyckj4h-9=ssdu&s!y42s7%bv#k+d(!n8u(s&1ifi)fo2degIT'

app = Flask(__name__)
bcrypt = Bcrypt(app)
login = flask_login.LoginManager()
login.init_app(app)
app.config.from_object(__name__)
app.config.from_envvar('config.ini', silent=True)


# TODO: Add more syntax comments

# DB Stuffs

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# TODO: add bcrypt to validation
def login_validate(form, field):
    fpass = form["password"]
    dbuser = query_db('SELECT username FROM users WHERE username = ?', (field.data,), one=True)
    dbpass = query_db('SELECT password FROM users WHERE username = ? AND password = ?', [field.data, fpass.data],
                      one=True)
    if dbuser is None:
        flash("Check that you entered everything correctly", "error")
        raise ValidationError("No such user")
    elif dbpass is None:
        flash("Check that you entered everything correctly", "error")
        raise ValidationError("Incorrect Password")


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(), login_validate])
    password = PasswordField('password', validators=[DataRequired()])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# ROUTES

# TODO: update all dis to be more api-style
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            error = "It worked with success"
            return render_template('login.html', form=form, error=error)
        else:
            error = "It worked with error"
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form, error=error)


# TODO: CREATE LOGOUT SYSTEM
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# TODO: DEBUG: REMOVE THIS: ADD FIRST RUN OVERRIDE FOR LOGIN PAGE TO CREATE ADMIN ACCOUNT


@app.route('/makeadmin')
def makeadmin():
    g.db.execute('insert into users (username, password, email) values (?, ?, ?)',
                 ["admin", "admin", "admin@admin.com"])
    g.db.commit()
    db = get_db()
    cur = db.execute('select username, password from users order by id desc')
    entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    return render_template('makeadmin.html', entries=entries)


# TODO: DEBUG: REMOVE THIS: MAKE USER MANAGER FOR ADMIN


@app.route('/listusers')
def listusers():
    db = get_db()
    cur = db.execute('select username, password from users order by id desc')
    entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    return render_template('makeadmin.html', entries=entries)


if __name__ == '__main__':
    app.run(None, 8001)
