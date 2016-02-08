from flask_wtf import Form, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from app import bcrypt
from .models import *


def login_validate(form, field):
    """Validates the login form"""
    fpass = form["password"]
    dbuser = User.query.filter_by(username=field.data).first()
    if dbuser is None:
        raise ValidationError("Check that you entered everything correctly")
    elif not bcrypt.check_password_hash(dbuser.password, fpass.data):
        raise ValidationError("Check that you entered everything correctly")


def register_validate(form, field):
    """Validates the register form"""
    femail = form["email"]
    dbuser = User.query.filter_by(username=field.data).first()
    dbemail = User.query.filter_by(email=femail.data).first()
    if dbuser is not None:
        raise ValidationError("Someone stole your username! Guess you have to pick a different one.")
    elif dbemail is not None:
        raise ValidationError("Email already in use. If you forget your username or password you can reset that from"
                              " the login page.")


class LoginForm(Form):
    """Creates a login form when called"""
    username = StringField('Username', validators=[DataRequired(message="You forgot to enter a username! You ok?"),
                                                   login_validate])
    password = PasswordField('Password', validators=[DataRequired(message="You forgot to enter a password! You ok?")])
    remember = BooleanField('Remember Me')


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
    email = StringField('Email', validators=[DataRequired(message='You need an email so we can contact you, give you '
                                                                  'notifications, and verify your account is not spam. '
                                                                  'Don\'t worry, we won\'t spam you or give your email '
                                                                  'away to anyone'),
                                             Email(message='Whoops, looks like you forgot to put an @ sign or maybe a'
                                                           ' .com? Just check to see if you typed that in right.')])
    type = SelectField('type', choices=[('admin', 'Admin'), ('student', 'Student'), ('parent', 'Parent')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='Something makes me think you might be a robot! Or else I '
                                                             'may have made an error... try again please.')])
