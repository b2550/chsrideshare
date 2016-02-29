from app import bcrypt
from flask import url_for, Markup, flash
from flask.ext.login import current_user
from flask_wtf import Form, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SelectField, BooleanField, HiddenField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from .models import *


# region Validators
def login_validate(form, field):
    """
    Validates the login form
    Ensures user has verified account via email and has entered their username and password correctly
    """
    fpass = form["password"]
    dbuser = Users.query.filter_by(email=field.data).first()
    if dbuser is None:
        raise ValidationError("Check that you entered everything correctly")
    elif not bcrypt.check_password_hash(dbuser.password, fpass.data):
        raise ValidationError("Check that you entered everything correctly")
    elif not dbuser.active:
        raise ValidationError(Markup("You have not verified your account. If you didn't get the email, check your spam."
                                     " Click <a href=\'" + url_for('verifyuser') + "\'>here</a> to resend the email."))


def register_validate(form, field):
    """
    Validates the register form
    Makes sure that the email the user is registering with is not already used
    """
    dbuser = Users.query.filter_by(email=field.data).first()
    if dbuser is not None:
        raise ValidationError("Email already in use. If you forget your password you can reset that from"
                              " the login page.")


def resend_verify_validate(form, field):
    """
    Validates the form used to resend the verification email
    Makes sure the username exists in the database
    Makes sure the user has not already been validated
    """
    email = Users.query.filter_by(email=field.data).first()
    if email is None:
        raise ValidationError('Could not find that email on our servers. Make sure you typed the email you used'
                              ' to register.')
    elif email.active is True:
        raise ValidationError('User already validated.')


def request_form_validate(form, field):
    """Validates the request form"""
    requests = Users.query.join(Requests, Requests.user_destination == Users.id).filter(
        Requests.user_destination == current_user.id).all()
    sent = Users.query.join(Requests, Requests.user_origin == Users.id).filter(Requests.user_origin == current_user.id,
                                                                               Requests.accepted < 1).all()
    group = Groups.query.filter_by(id=form['group_id'].data).first()

    if group is None:
        raise ValidationError('This group does not exist')

    for req in sent:
        if req.receiver.id == field.data and req.group_id == form['group_id'].data:
            flash('You already sent a request to this user')
            raise ValidationError('You already sent a request to this user')
    for req in requests:
        if req.sender.id == field.data and req.group_id == form['group_id'].data:
            flash('This user already sent a request to you')
            raise ValidationError('This user already sent a request to you')


def accept_form_validate(form, field):
    """Validates the accept request form"""
    requests = Users.query.join(Requests, Requests.user_destination == Users.id).filter(
        Requests.user_destination == current_user.id).all()
    for r in requests:
        for req in r.requests:
            if req.sender.id != int(field.data) and req.receiver.id != current_user.id and req.group_id != form[
                'group_id'].data:
                raise ValidationError('You are not logged in as the right user or that user did not send you a request')


def join_form_validate(form, field):
    if Groups.query.filter_by(join_id=field.data).first() is None:
        raise ValidationError('You must have entered the code wrong. Try again please.')
    for group in current_user.groups:
        if group.join_id == field.data:
            raise ValidationError('You are already a member of this group')


def notification_form_validate(form, field):
    notifications = Notifications.query.filter_by(user_id=current_user.id).all()
    if not notifications.contains(field.data):
        raise ValidationError('Not your notification')


# endregion


# region User System Forms
class LoginForm(Form):
    """
    Creates a user login form when called
    Returns:
        email: WTF Forms StringField with DataRequired validator and login_validate validator
        password: WTF Forms PasswordField with DataRequired validator
        remember: WTF Forms BooleanField (checkbox)
    References:
        Flask-WTF Form
        login_validate
    Examples:
        Email and password can be passed to user database table and remember can be used to create cookie session
    """
    email = StringField('Email', validators=[DataRequired(message="You forgot to enter your email! You ok?"),
                                             login_validate])
    password = PasswordField('Password', validators=[DataRequired(message="You forgot to enter a password! You ok?")])
    remember = BooleanField('Remember Me')


class RegisterForm(Form):
    """Creates a user registration form when called"""
    email = StringField('Email', validators=[DataRequired(message='You need an email so we can log you in, contact you,'
                                                                  ' give you notifications, and verify your account is'
                                                                  ' not spam. Don\'t worry, we won\'t spam you or give '
                                                                  'your email away to anyone'),
                                             Email(message='Whoops, looks like you forgot to put an @ sign or maybe a'
                                                           ' .com? Just check to see if you typed that in right.'),
                                             register_validate])
    password = PasswordField('Password', validators=[DataRequired(
        message='You need a password silly, or else people can just login as you by knowing your email')])
    firstname = StringField('First Name', validators=[DataRequired(
        message='This is so other people know who you are. Please give us a name.')])
    lastname = StringField('Last Name', validators=[DataRequired(
        message='This is so other people know who you are. Please give us a name.')])
    passwordvalidate = PasswordField('Repeat Password', validators=[DataRequired(
        message='You need to fill this out! We just need to check that you didn\'t mess up your password'
                ' by accident.'), EqualTo('password', message='Oh jeez, looks like you mistyped your password.'
                                                              ' Do me a big favor and type it in to both password'
                                                              ' boxes again so I don\'t have to reset it for you'
                                                              ' later.')])
    type = SelectField('What are you?', choices=[('student', 'Student'), ('parent', 'Parent')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Something makes me think you might be a robot! Or else I '
                                                             'may have made an error... try again please.')])


class ResendVerifyFrom(Form):
    """Creates a form to resend the user verification email when called"""
    email = StringField('Email', validators=[DataRequired(message='You gotta enter an email!'),
                                             Email(message='Whoops, looks like you forgot to put an @ sign or maybe a'
                                                           ' .com? Just check to see if you typed that in right.'),
                                             resend_verify_validate])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Something makes me think you might be a robot! Or else I '
                                                             'may have made an error... try again please.')])


# endregion


# region Request System Forms
class RequestForm(Form):
    """Creates a request form when called"""
    user_destination = HiddenField('User ID', validators=[DataRequired(message='Error: user may not exist.'),
                                                          request_form_validate])
    message = TextAreaField('Message')
    group_id = SelectField('Group', coerce=int)


# TODO: Integrate cancel request feature
class CancelRequestForm(Form):
    """Creates a cancel request form when called"""
    pass


# TODO: Integrate deny request feature
class DenyRequestForm(Form):
    """Creates a deny request form when called"""
    pass


class AcceptForm(Form):
    """Creates an accept request form when called"""
    user_origin = HiddenField('Origin User ID',
                              validators=[DataRequired(message='Error: user may not exist'), accept_form_validate])
    group_id = HiddenField('Group ID', validators=[DataRequired(message='Group does not exist')])


# endregion


# region Group System
class CreateGroupForm(Form):
    name = StringField('Group Name', validators=[DataRequired(message='You must enter a group name')])


class JoinGroupForm(Form):
    join_id = StringField('Group Code',
                          validators=[DataRequired(message='You must enter a 6 digit group code'), join_form_validate])


# TODO: Integrate leave group feature
class LeaveGroupForm(Form):
    # Can't leave group as group manager
    pass


# TODO: Integrate remove user from group feature (set 1 user as group admin)
class RemoveFromGroupForm(Form):
    pass


# TODO: Integrate delete group feature (can only be done by group admin)
class DeleteGroupForm(Form):
    pass


# endregion


class AddressForm(Form):
    """Creates a form to set or change a user address when called"""
    streetnum = HiddenField('Street Number', validators=[DataRequired()])
    streetaddress = HiddenField('Street Address', validators=[DataRequired()])
    city = HiddenField('City', validators=[DataRequired()])
    state = HiddenField('State', validators=[DataRequired()])
    zip = HiddenField('Zip Code', validators=[DataRequired()])
    country = HiddenField('Country', validators=[DataRequired()])


class RangeForm(Form):
    """Creates a user search range form when called"""
    range = DecimalField('Search Radius (Miles)', places=2, validators=[DataRequired()])


class DismissNotificationForm(Form):
    id = HiddenField('Notification ID', validators=[DataRequired('Notification doesn\'t exist')])
