from bookmarks import app
from flask import flash, render_template, request, redirect, url_for, abort
from bookmarks.database import db_session
from bookmarks.models import User, Bookmark
from bookmarks.modules.hex_gen import hex_gen


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def front_page():
    return 'home'


@app.route('/add_bookmark/', methods=['GET', 'POST'])
def add_bookmark():
    if request.method == 'POST':
        short = request.form['short']
        link = request.form['link']
        b = Bookmark(short, link, user_id=1)
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
        u = User(username, name, email)
        db_session.add(u)
        db_session.commit()
        flash('Successfully registered {} {} {}'.format(username, name, email),
              category='info')
        # return redirect(url_for('front_page'), 303)
        return redirect(url_for('register_user'), 303)
    else:
        return render_template('register_user.html')


@app.route('/<string:short>', methods=['GET'])
def get_bookmark(short):
    if len(short) == 6:
        b = Bookmark.query.filter(Bookmark.short == short).first()
        if b is not None:
            return b.link
    abort(404)
