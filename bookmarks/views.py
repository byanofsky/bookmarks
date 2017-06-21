from bookmarks import app
from flask import flash, render_template, request, redirect, url_for


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
