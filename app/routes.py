import binascii

import flask_sijax
import os
from app import app, bcrypt, login_manager, mail
from flask import request, g, redirect, url_for, render_template, flash
from flask.ext.mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, ResendVerifyFrom, AddressForm
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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')


@flask_sijax.route(app, '/dashboard')
@login_required
def dashboard():
    if current_user.address is None:
        form = AddressForm()
        return render_template('dashboard.html', address_form=form)
    return render_template('dashboard.html')


# TODO: Take in value of address and format it for database (try to get this to happen with AJAX)
@app.route('/setaddress', methods=['GET', 'POST'])
def address():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user, remember=form.remember.data)
            flash('Logged in as ' + current_user.firstname + " " + current_user.lastname)
            return render_template('login.html', login_form=form)
    return render_template('login.html', login_form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            password = bcrypt.generate_password_hash(form.password.data)
            uid = binascii.hexlify(os.urandom(32)).decode()
            user = User(form.email.data, password, form.firstname.data, form.lastname.data, form.type.data, uid,
                        active=False)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=form.email.data).first()
            msg = Message(subject="Activate CHS Ride Share Account", sender=("Ride Share",
                                                                             "validation@rideshare.org"))
            msg.html = render_template('verify_email.html', suid=user)
            msg.recipients = [form.email.data]
            mail.send(msg)
            flash('Registered the user ' + form.firstname.data + " " + form.lastname.data +
                  '! Check your email to activate your account.')
            return render_template('register.html', register_form=form)
        else:
            flash('did not validate')
            return render_template('register.html', register_form=form)
    return render_template('register.html', register_form=form)


@app.route('/verify', methods=['GET', 'POST'], defaults={'uid': 'nouser'})
@app.route('/verify/<uid>')
def verifyuser(uid):
    form = ResendVerifyFrom()
    vid = User.query.filter_by(uid=uid).first()
    if vid.active is True:
        flash('User already verified')
        return redirect(url_for('login'))
    elif uid is not 'nouser':
        if vid:
            if vid.uid == uid:
                vid.active = True
                db.session.commit()
                flash('User Verified!')
                return redirect(url_for('login'))
            else:
                flash("Did not verify user")
                return render_template('verify.html', verify_form=form)
    elif form.validate_on_submit():
        suid = User.query.filter_by(email=form.email.data).first()
        msg = Message(subject="Activate CHS Ride Share Account", sender=("Ride Share", "validation@rideshare.org"))
        msg.html = render_template('verify_email.html', suid=suid)
        msg.recipients = [form.email.data]
        mail.send(msg)
        flash('Check your email to activate your account.')
        return redirect(url_for('login'))
    else:
        return render_template('verify.html', verify_form=form)

# @app.route('/listusers')
# def listusers():
#     entries = User.query.order_by(User.email)
#     return render_template('makeadmin.html', entries=entries)
#
#
# @app.route('/initdb')
# def init_database():
#     db.create_all()
#     return render_template('test.html', output='database created')
#
#
# @app.route('/protected')
# @login_required
# def testprotectedpage():
#     return render_template('test.html', output='Logged in')
