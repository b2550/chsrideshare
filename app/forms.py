from app import bcrypt
from flask import url_for, Markup, flash
from flask.ext.login import current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, BooleanField, HiddenField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from .models import *


def login_validate(form, field):
    """Validates the login form"""
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
    """Validates the register form"""
    dbuser = Users.query.filter_by(email=field.data).first()
    if dbuser is not None:
        raise ValidationError("Email already in use. If you forget your password you can reset that from"
                              " the login page.")


def resendvalidation_validate(form, field):
    email = Users.query.filter_by(email=field.data).first()
    if email is None:
        raise ValidationError('Could not find that email on our servers. Make sure you typed the email you used'
                              ' to register.')
    elif email.active is True:
        raise ValidationError('User already validated.')


class LoginForm(Form):
    """Creates a login form when called"""
    email = StringField('Email', validators=[DataRequired(message="You forgot to enter your email! You ok?"),
                                             login_validate])
    password = PasswordField('Password', validators=[DataRequired(message="You forgot to enter a password! You ok?")])
    remember = BooleanField('Remember Me')


class AddressForm(Form):
    streetnum = HiddenField('Street Number', validators=[DataRequired()])
    streetaddress = HiddenField('Street Address', validators=[DataRequired()])
    city = HiddenField('City', validators=[DataRequired()])
    state = HiddenField('State', validators=[DataRequired()])
    zip = HiddenField('Zip Code', validators=[DataRequired()])
    country = HiddenField('Country', validators=[DataRequired()])


# TODO: ADD RECAPCHA BACK
class RegisterForm(Form):
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
    type = SelectField('type', choices=[('admin', 'Admin'), ('student', 'Student'), ('parent', 'Parent')])
    # recaptcha = RecaptchaField(validators=[Recaptcha(message='Something makes me think you might be a robot! Or else I '
    #                                                         'may have made an error... try again please.')])


# TODO: ADD RECAPCHA BACK
class ResendVerifyFrom(Form):
    email = StringField('Email', validators=[DataRequired(message='You gotta enter an email!'),
                                             Email(message='Whoops, looks like you forgot to put an @ sign or maybe a'
                                                           ' .com? Just check to see if you typed that in right.'),
                                             resendvalidation_validate])
    # recaptcha = RecaptchaField(validators=[Recaptcha(message='Something makes me think you might be a robot! Or else I '
    #                                                         'may have made an error... try again please.')])


def RequestFormValidateOrigin(form, field):
    requests = Users.query.join(Requests, Requests.user_destination == Users.id).filter(
        Requests.user_destination == current_user.id).all()
    sent = Users.query.join(Requests, Requests.user_origin == Users.id).filter(Requests.user_origin == current_user.id,
                                                                               Requests.accepted < 1).all()
    for req in sent:
        if req.receiver.id == field.data:
            flash('You already sent a request to this user')
            raise ValidationError('You already sent a request to this user')
    for req in requests:
        if req.sender.id == field.data:
            flash('This user already sent a request to you')
            raise ValidationError('This user already sent a request to you')


class RequestForm(Form):
    user_destination = HiddenField('User ID', validators=[DataRequired(message='Error: user may not exist.'),
                                                          RequestFormValidateOrigin])
    message = TextAreaField('Message')


# TODO: Integrate cancel and deny features
class CancelRequestForm(Form):
    pass


class DenyRequestForm(Form):
    pass


class AcceptForm(Form):
    user_origin = HiddenField('Origin User ID', validators=[DataRequired(message='Error: user may not exist')])


class RangeForm(Form):
    range = DecimalField('Search Radius (Miles)', places=2)
