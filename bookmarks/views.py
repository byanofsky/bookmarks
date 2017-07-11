import random
import string
import requests
from bookmarks import app, bcrypt, login_manager
from flask import flash, render_template, request, redirect, url_for, abort
from bookmarks.database import db_session
from bookmarks.models import User, Bookmark
import flask_login
from bookmarks.forms import BookmarkForm, RegisterForm

# Create user agent for requests
USER_AGENT = '{}/{}'.format(
    app.config['USER_AGENT_NAME'],
    app.config['VERSION_NUMBER'])


def hex_gen():
    # Generates a six character string of upper/lower letters and digits
    return ''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(6))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    if not User.query.filter(User.id == user_id).one_or_none():
        return
    user = flask_login.UserMixin()
    user.id = user_id
    return user


@app.route('/', methods=['GET'])
def front_page():
    bookmarks = Bookmark.query.all()
    return render_template('front_page.html', bookmarks=bookmarks)


@app.route('/add_bookmark/', methods=['GET', 'POST'])
@flask_login.login_required
def add_bookmark():
    # Generate a possible id
    b_id = hex_gen()
    form = BookmarkForm(b_id=b_id)
    if form.validate_on_submit() and request.method == 'POST':
        b_id = form.b_id.data
        link = form.link.data
        # T/F for following link redirects
        follow_redirects = form.follow_redirects.data
        # Test that link works, or return error to user
        try:
            r = requests.get(link, headers={'user-agent': USER_AGENT},
                             allow_redirects=follow_redirects)
            r.raise_for_status()
        # Exceptions for 400 or 500 errors
        except requests.exceptions.HTTPError as e:
            flash('Please check your link. It leads to this error: {}.'
                  .format(e),
                  category='error')
        # Connection errors
        except requests.exceptions.ConnectionError:
            flash('Could not connect to your link. Please check URL.')
        # Timeout errors
        except requests.exceptions.Timeout:
            flash('There was a timeout error. Please check URL.')
        # Too many redirects
        except requests.exceptions.TooManyRedirects:
            flash('Exceeded max number of redirects. Please check URL.')
        # All other requests-related exceptions
        except requests.exceptions.RequestException as e:
            flash('Please check your link. It leads to this error: {}.'
                  .format(e),
                  category='error')
        # No errors when requesting link, so add to database
        else:
            url = r.url  # Get final url (from redirects)
            b = Bookmark(b_id, link=url, user_id=flask_login.current_user.id)
            db_session.add(b)
            db_session.commit()
            flash('Successfully added {} {}'.format(b_id, url),
                  category='info')
            return redirect(url_for('add_bookmark'), 303)
    # If it exists, keep regenerating
    while Bookmark.query.filter(Bookmark.id == b_id).first() is not None:
        b_id = hex_gen()
    return render_template('add_bookmark.html', form=form, b_id=b_id)


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
                category='error')
        if User.query.filter(User.email == email).one_or_none() is not None:
            errors['email_exists'] = True
            flash('A user already exists with the email {}'.format(email),
                  category='error')
        if not errors:
            pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            u = User(username, name, email, pw_hash)
            db_session.add(u)
            db_session.commit()
            flash('Successfully registered {} {} {}'.format(username, name, email),
                  category='info')
            user = flask_login.UserMixin()
            user.id = u.id
            flask_login.login_user(user)
            return redirect(url_for('front_page'), 303)
    return render_template('register_user.html', form=form, errors=errors)


@app.route('/login_user/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = User.query.filter(User.username == username).one_or_none()
        if u is not None:
            if bcrypt.check_password_hash(u.pw_hash, password):
                user = flask_login.UserMixin()
                user.id = u.id
                flask_login.login_user(user)
                flash('Successfully logged in {}'.format(username),
                      category='info')
                return redirect(url_for('login_user'), 303)
            else:
                flash('Password incorrect')
        else:
            flash('User does not exist')
        return redirect(url_for('login_user'))
    else:
        return render_template('login_user.html')


@app.route('/logout_user/', methods=['GET', 'POST'])
def logout_user():
    if request.method == 'POST':
        flask_login.logout_user()
        flash('Successfully logged out',
              category='info')
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
