import random
import requests
import string

from flask import (flash, render_template, request, redirect, url_for, abort,
                   Markup)
import flask_login

from bookmarks import app, bcrypt, login_manager
from bookmarks.database import db_session
from bookmarks.forms import BookmarkForm, RegisterForm, LoginForm
from bookmarks.models import User, Bookmark

# Create user agent for requests
USER_AGENT = '{}/{}'.format(
    app.config['USER_AGENT_NAME'],
    app.config['VERSION_NUMBER'])
# Timeout for requests library
TIMEOUT = app.config['TIMEOUT']


def hex_gen():
    # Generates a six character string of upper/lower letters and digits
    return ''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(6))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    u = User.query.filter(User.id == user_id).one_or_none()
    if not u:
        return None
    user = flask_login.UserMixin()
    user.id = u.id
    user.name = u.name
    return user


@app.route('/', methods=['GET'])
def front_page():
    bookmarks = Bookmark.query.order_by(Bookmark.hits.desc()).limit(5).all()
    return render_template('front_page.html', bookmarks=bookmarks)


@app.route('/add_bookmark/', methods=['GET', 'POST'])
@flask_login.login_required
def add_bookmark():
    form = BookmarkForm(link='http://')
    if form.validate_on_submit() and request.method == 'POST':
        # Get form data
        link = form.link.data
        follow_redirects = form.follow_redirects.data  # T/F for following link redirects
        # Test that link works, or return error to user
        try:
            r = requests.get(link, headers={'user-agent': USER_AGENT},
                             allow_redirects=follow_redirects,
                             timeout=TIMEOUT)
            r.raise_for_status()
        # Exceptions for 400 or 500 errors
        except requests.exceptions.HTTPError as e:
            flash('Please check your link. It leads to this error: {}.'
                  .format(e),
                  category='danger')
        # Missing schema
        except requests.exceptions.MissingSchema as e:
            flash('No schema. Did you mean http://{}?'.format(link),
                  category='danger')
        # Timeout errors
        except requests.exceptions.Timeout:
            flash('There was a timeout error. Please check URL.',
                  category='danger')
        # Connection errors
        except requests.exceptions.ConnectionError:
            flash('Could not connect to your link. Please check URL.',
                  category='danger')
        # Too many redirects
        except requests.exceptions.TooManyRedirects:
            flash('Exceeded max number of redirects. Please check URL.',
                  category='danger')
        # All other requests-related exceptions
        except requests.exceptions.RequestException as e:
            flash('Please check your link. It leads to this error: {}.'
                  .format(e),
                  category='danger')
        # No errors when requesting link, so add to database
        else:
            # Generate a possible id
            b_id = hex_gen()
            # If it exists, keep regenerating
            while (Bookmark.query.filter(Bookmark.id == b_id).one_or_none()
                    is not None):
                b_id = hex_gen()
            url = r.url  # Get final url (from redirects)
            url_root = request.url_root
            b = Bookmark(b_id, link=url, user_id=flask_login.current_user.id)
            db_session.add(b)
            db_session.commit()
            msg_uf = ('Successfully added {0}. Your short link is ' +
                      '<a target="_blank" href="{1}">{1}</a>.')
            msg = msg_uf.format(url, url_root+b_id)
            flash(Markup(msg), category='success')
            return redirect(url_for('add_bookmark'), 303)
    return render_template('add_bookmark.html', form=form)


@app.route('/register_user/', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    errors = {}
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        name = form.name.data
        email = form.email.data
        # Check if username and email already exist
        if User.query.filter(User.username == username).one_or_none() is not None:
            errors['username_exists'] = True
            flash(
                'A user already exists with the username {}'.format(username),
                category='danger')
        if User.query.filter(User.email == email).one_or_none() is not None:
            errors['email_exists'] = True
            flash('A user already exists with the email {}'.format(email),
                  category='danger')
        if not errors:
            pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            u = User(username, name, email, pw_hash)
            db_session.add(u)
            db_session.commit()
            flash('Successfully registered {} {} {}'.format(username, name, email),
                  category='success')
            user = flask_login.UserMixin()
            user.id = u.id
            flask_login.login_user(user)
            return redirect(url_for('front_page'), 303)
    return render_template('register_user.html', form=form, errors=errors)


@app.route('/login_user/', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        # Attempt to get user record
        u = User.query.filter(User.username == username).one_or_none()
        # Check if user exists
        if u is not None:
            # Check if password is correct
            if bcrypt.check_password_hash(u.pw_hash, password):
                # Log user in
                user = flask_login.UserMixin()
                user.id = u.id
                flask_login.login_user(user)
                flash('Successfully logged in {}'.format(username),
                      category='success')
                return redirect(url_for('front_page'), 303)
            # Password is not correct, flash message
            else:
                flash('Password incorrect')
        # User does not exist, flash message
        else:
            flash('User does not exist')
    return render_template('login_user.html', form=form)


@app.route('/logout_user/', methods=['GET', 'POST'])
def logout_user():
    if request.method == 'POST':
        flask_login.logout_user()
        flash('Successfully logged out',
              category='success')
        return redirect(url_for('front_page'), 303)
    else:
        return render_template('logout_user.html')


@app.route('/<string:b_id>', methods=['GET'])
def get_bookmark(b_id):
    if len(b_id) == 6:
        b = Bookmark.query.filter(Bookmark.id == b_id).one_or_none()
        if b is not None:
            b.hits += 1
            db_session.add(b)
            db_session.commit()
            return redirect(b.link, 307)
    abort(404)
