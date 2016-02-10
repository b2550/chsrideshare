from app import bcrypt
from flask import url_for, Markup
from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from .models import *


def login_validate(form, field):
    """Validates the login form"""
    fpass = form["password"]
    dbuser = User.query.filter_by(email=field.data).first()
    if dbuser is None:
        raise ValidationError("Check that you entered everything correctly")
    elif not bcrypt.check_password_hash(dbuser.password, fpass.data):
        raise ValidationError("Check that you entered everything correctly")
    elif not dbuser.active:
        raise ValidationError(Markup("You have not verified your account. If you didn't get the email, check your spam."
                                     " Click <a href=\'" + url_for('verifyuser') + "\'>here</a> to resend the email."))


def register_validate(form, field):
    """Validates the register form"""
    dbuser = User.query.filter_by(email=field.data).first()
    if dbuser is not None:
        raise ValidationError("Email already in use. If you forget your password you can reset that from"
                              " the login page.")


def resendvalidation_validate(form, field):
    email = User.query.filter_by(email=field.data).first()
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
    streetnum = StringField('Street Number', validators=[DataRequired()])
    streetaddress = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('Zip Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])


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
