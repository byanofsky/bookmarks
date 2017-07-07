import random
import string
from bookmarks import app, bcrypt, login_manager
from flask import flash, render_template, request, redirect, url_for, abort
from bookmarks.database import db_session
from bookmarks.models import User, Bookmark
import flask_login


def hex_gen():
    # Generates a six character string of upper/lower letters and digits
    return ''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(6))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    if not User.query.filter(User.id == user_id).first():
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
    if request.method == 'POST':
        b_id = request.form['b_id']
        link = request.form['link']
        b = Bookmark(b_id, link, user_id=flask_login.current_user.id)
        db_session.add(b)
        db_session.commit()
        flash('Successfully added {} {}'.format(b_id, link),
              category='info')
        return redirect(url_for('add_bookmark'), 303)
    else:
        # Generate a possible id
        b_id = hex_gen()
        # If it exists, keep regenerating
        while Bookmark.query.filter(Bookmark.id == b_id).first() is not None:
            b_id = hex_gen()
        return render_template('add_bookmark.html', b_id=b_id)


@app.route('/register_user/', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        u = User(username, name, email, pw_hash)
        db_session.add(u)
        db_session.commit()
        flash('Successfully registered {} {} {}'.format(username, name, email),
              category='info')
        # return redirect(url_for('front_page'), 303)
        return redirect(url_for('register_user'), 303)
    else:
        return render_template('register_user.html')


@app.route('/login_user/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = User.query.filter(User.username == username).first()
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
        b = Bookmark.query.filter(Bookmark.id == b_id).first()
        if b is not None:
            b.hits += 1
            db_session.add(b)
            db_session.commit()
            return redirect(b.link, 307)
    abort(404)
