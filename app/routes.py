import binascii
import math

import os
from app import app, bcrypt, login_manager, mail
from flask import request, g, redirect, url_for, render_template, flash
from flask.ext.mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from .apihandler import geocodeing_parser
from .forms import LoginForm, RegisterForm, ResendVerifyFrom, AddressForm, RequestForm, AcceptForm, RangeForm
from .models import *


@app.before_request
def get_login_status():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('test.html', output='Unauthorised')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.address is None:
        form = AddressForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                address = form.streetnum.data + " " + form.streetaddress.data + ", " + form.city.data + ", " + form.state.data + ", " + form.country.data
                user = Users.query.filter_by(email=current_user.email).first()
                user.address = address
                db.session.add(user)
                db.session.commit()
                flash('Address Updated')
                return redirect(url_for('dashboard'))
            else:
                flash('That is not a valid address')
                return render_template('dashboard.html', address_form=form)
        return render_template('dashboard.html', address_form=form)
    elif current_user.latitude is None or current_user.longitude is None:
        geocode = geocodeing_parser(current_user.email)
        if geocode['error'] is None:
            user = Users.query.filter_by(email=current_user.email).first()
            user.latitude = geocode['latitude']
            user.longitude = geocode['longitude']
            user.address = geocode['address']
            db.session.add(user)
            db.session.commit()
            flash('You can now be found by other users')
            return redirect(url_for('dashboard'))
        else:
            # TODO: Update this to real error handler
            return {
                'ZERO_RESULTS': 'Your address is not a real location. Please update.',
                'OVER_QUERY_LIMIT': 'We can\'t proccess your request right now. Try again in a few minutes. If the problem persists, try again tomarrow.',
                'REQUEST_DENIED': 'Something is wrong on our end so we can\'t proccess your request right now',
                'INVALID_REQUEST': 'Your address was not saved to our database correctly. Please update it.',
                'UNKNOWN_ERROR': 'Something is seriously broken so we can\'t proccess your request right now'
            }[geocode['error']]
    else:
        # TODO: Check if user is already in group to prevent problems
        request_form = RequestForm()
        accept_form = AcceptForm()
        range_form = RangeForm()
        query_range = 1

        canidates = []
        requests = Users.query.join(Requests, Requests.user_destination == Users.id).filter(
            Requests.user_destination == current_user.id, Requests.accepted < 1).all()
        sent = Users.query.join(Requests, Requests.user_origin == Users.id).filter(
            Requests.user_origin == current_user.id, Requests.accepted < 1).all()
        users = Users.query.all()

        if request.method == 'POST':
            if request_form.validate_on_submit():
                req = Requests(current_user.id, request_form.user_destination.data, request_form.message.data)
                db.session.add(req)
                db.session.commit()
                flash('Request Sent')
                return redirect(url_for('dashboard'))
            if accept_form.validate_on_submit():
                req = Requests.query.filter_by(user_origin=int(accept_form.user_origin.data),
                                               user_destination=current_user.id).first()
                req.accepted = 1
                db.session.add(req)
                db.session.commit()
                flash('Request Accepted')
                if current_user.group_id is None and req.sender.group_id is None:
                    group = Groups(req.sender.id)
                    db.session.add(group)
                    db.session.commit()
                    groups = Groups.query.filter_by(primary_user=req.sender.id).first()
                    user1 = Users.query.filter_by(id=current_user.id).first()
                    user2 = Users.query.filter_by(id=req.sender.id).first()
                    user1.group_id = groups.id
                    user2.group_id = groups.id
                    flash('A group has been created for you and ' + req.sender.firstname)
                    notification = Notifications(req.sender.id,
                                                 current_user.firstname + ' has accepted your request, and a group has been created for you')
                    db.session.add_all([user1, user2, notification])
                    db.session.commit()

                if current_user.group_id is not None and req.sender.group_id is None:
                    print 'add the requester to the group'
                if current_user.group_id is not None and req.sender.group_id is not None:
                    print 'one user will have to leave their current group'

                # TODO: Add text to notify receiver if user is joining their group, if they are joining a group, or if they will have to leave their current group
                # TODO: Call group manager handler (deletes request when complete)
                # TODO: Notify origin user that request was accepted via email and notification (create notifications table)
                return redirect(url_for('dashboard'))
            if range_form.validate_on_submit():
                query_range = range_form.range.data

        for user in users:
            if (3959 * math.acos(math.cos(math.radians(float(current_user.latitude))) * math.cos(
                    math.radians(user.latitude)) * math.cos(
                        math.radians(user.longitude) - math.radians(float(current_user.longitude))) + math.sin(
                    math.radians(float(current_user.latitude))) * math.sin(math.radians(user.latitude)))) < query_range:
                if user.requests or user.sentrequests:
                    for req in user.requests:
                        if req.sender.id != current_user.id and canidates.count(user) < 1:
                            canidates.append(user)
                else:
                    canidates.append(user)

        return render_template(
            'dashboard.html',
            canidates=canidates,
            requests=requests,
            sent=sent,
            request_form=request_form,
            accept_form=accept_form,
            range_form=range_form,
            query_range=query_range
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            login_user(user, remember=form.remember.data)
            flash('Logged in as ' + current_user.firstname + " " + current_user.lastname)
            return redirect(url_for('index'))
    elif current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', login_form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        if form.validate_on_submit():
            password = bcrypt.generate_password_hash(form.password.data)
            uid = binascii.hexlify(os.urandom(32)).decode()
            user = Users(form.email.data, password, form.firstname.data, form.lastname.data, form.type.data, uid,
                         active=False)
            db.session.add(user)
            db.session.commit()
            user = Users.query.filter_by(email=form.email.data).first()
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
    vid = Users.query.filter_by(uid=uid).first()
    if uid is not 'nouser':
        if vid:
            if vid.active is True:
                flash('User already verified')
                return redirect(url_for('login'))
            elif vid.uid == uid:
                vid.active = True
                db.session.commit()
                flash('User Verified!')
                return redirect(url_for('login'))
            else:
                flash("Did not verify user")
                return render_template('verify.html', verify_form=form)
    elif form.validate_on_submit():
        suid = Users.query.filter_by(email=form.email.data).first()
        msg = Message(subject="Activate CHS Ride Share Account", sender=("Ride Share", "validation@rideshare.org"))
        msg.html = render_template('verify_email.html', suid=suid)
        msg.recipients = [form.email.data]
        mail.send(msg)
        flash('Check your email to activate your account.')
        return redirect(url_for('login'))
    else:
        return render_template('verify.html', verify_form=form)

