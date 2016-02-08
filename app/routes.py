import os

from flask import request, g, redirect, url_for, render_template, flash
from flask.ext.mail import Message
from flask_login import login_user, logout_user, login_required, current_user

from app import app, bcrypt, login_manager, mail
from .forms import LoginForm, RegisterForm
from .models import *


@app.before_request
def get_login_status():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('test.html', output='Unauthorised')


@app.route('/')
def index():
    return render_template('page.html')


# TODO: update all dis to be more api-style
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Logged in as ' + current_user.username)
            user = User.query.filter_by(username=form.username.data).first()
            login_user(user, remember=form.remember.data)
            return render_template('login.html', login_form=form)
    return render_template('login.html', login_form=form)


# TODO: CREATE LOGOUT SYSTEM
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


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
            uid = os.urandom(32)
            user = User(username, password, email, utype, uid, active=True)
            db.session.add(user)
            db.session.commit()
            msg = Message(sender=("Squizit Account Validation", "validation@squizit.org"))
            msg.html = "<b>To verify your account, go to the link below</b>" \
                       "<br><a href=\'" + url_for('verifyuser') + uid + "\'>Validate</a>"
            msg.recipients = [form.email]
            mail.send(msg)
            flash('Registered the user ' + username)
            return render_template('register.html', register_form=form)
        else:
            flash('did not validate')
            return render_template('register.html', register_form=form)
    return render_template('register.html', register_form=form)


# TODO: DEBUG: REMOVE THIS: MAKE USER MANAGER FOR ADMIN

@app.route('/verify/<uid>')
def verifyuser(uid):
    vid = User.query.filter_by(uid=uid).first
    if vid:
        if vid.uid == uid:
            vid.set_active(True)
        else:
            flash("Did not verify user")
            return redirect(url_for('login'))
    else:
        flash("User validation ID does not exist")
        return redirect(url_for('login'))


# TODO: DEBUG: REMOVE THIS: MAKE USER MANAGER FOR ADMIN


@app.route('/listusers')
def listusers():
    entries = User.query.order_by(User.username)
    return render_template('makeadmin.html', entries=entries)


@app.route('/initdb')
def init_database():
    db.create_all()
    return render_template('test.html', output='database created')


@app.route('/protected')
@login_required
def testprotectedpage():
    return render_template('test.html', output='Logged in')
