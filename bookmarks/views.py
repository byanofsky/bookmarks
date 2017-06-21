from bookmarks import app
from flask import flash, render_template, request, redirect, url_for
from bookmarks.database import db_session
from bookmarks.models import User


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
        flash('Successfully added {} {}'.format(short, link),
              category='info')
        return redirect(url_for('front_page'), 303)
    else:
        return render_template('add_bookmark.html')


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
