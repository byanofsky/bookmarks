from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, URL


class BookmarkForm(FlaskForm):
    b_id = StringField('Bookmark ID', [
        Length(min=6,
               max=6,
               message='Bookmark ID must be 6 characters long')
    ])
    link = StringField('Link', [
        DataRequired(),
        URL(message='Link must be a properly formatted URL')
    ])
    follow_redirects = BooleanField('Follow Redirects?')


class RegisterForm(FlaskForm):
    username = StringField('Username', [
        Length(min=4,
               max=25,
               message='Username must be between 4 and 25 characters')
    ])
    name = StringField('Name', [DataRequired()])
    email = StringField('Email Address', [Email(), Length(min=6, max=35)])
    password = PasswordField('New Password', [
        Length(min=5, max=18),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS')
