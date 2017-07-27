from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import (DataRequired, Length, EqualTo, Email, Regexp,
                                URL)


class BookmarkForm(FlaskForm):
    link = StringField('Link', [
        DataRequired(),
        URL(message='Link must be a properly formatted URL')
    ])
    follow_redirects = BooleanField('Follow Redirects?')


class BookmarkFormCustomID(FlaskForm):
    b_id = StringField('Bookmark ID', [
        Length(min=6,
               max=6,
               message='Bookmark ID must be 6 characters long'),
        # Validate only lowercase letters and numbers
        Regexp('^[0-9a-z]{1,6}$',
               message='Can only include lowercase letters and digits')
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
        Length(min=5, max=18,
               message='Password must be 5 to 18 characters long'),
        # Check for 1 lower, 1 upper, and number
        Regexp(
            '^(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z]).{5,18}$',
            message=('Password must include at least one lowercase ' +
                     'letter, one uppercase letter, and one number.')
        )
    ])
    confirm = PasswordField('Repeat Password', [
        EqualTo('password', message='You must confirm your password')
    ])
    accept_tos = BooleanField('I accept the TOS')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Please enter a username')
    ])
    password = PasswordField('Password', [
        DataRequired(message='Please enter a password')
    ])
