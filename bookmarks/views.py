from bookmarks import app, login_manager
from flask import flash, render_template, request, redirect, url_for, abort
from bookmarks.database import db_session
from bookmarks.models import User, Bookmark
from bookmarks.modules.hex_gen import hex_gen
import flask_login


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
def add_bookmark():
    if request.method == 'POST':
        short = request.form['short']
        link = request.form['link']
        b = Bookmark(short, link, user_id=4)
        db_session.add(b)
        db_session.commit()
        flash('Successfully added {} {}'.format(short, link),
              category='info')
        return redirect(url_for('add_bookmark'), 303)
    else:
        # Generate a possible short
        short = hex_gen()
        # If it exists, keep regenerating
        while Bookmark.query.filter(Bookmark.short == short).first() is not None:
            short = hex_gen()
        return render_template('add_bookmark.html', short=short)


@app.route('/register_user/', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        u = User(username, name, email, password)
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
            if u.check_password(password):
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


@app.route('/logout_user/')
def logout_user():
    flask_login.logout_user()
    return 'logged out'


@app.route('/<string:short>', methods=['GET'])
def get_bookmark(short):
    if len(short) == 6:
        b = Bookmark.query.filter(Bookmark.short == short).first()
        if b is not None:
            b.hits += 1
            db_session.add(b)
            db_session.commit()
            return redirect(b.link)
    abort(404)
