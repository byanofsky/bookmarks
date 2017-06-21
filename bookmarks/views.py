from bookmarks import app
from flask import render_template, request


@app.route('/', methods=['GET'])
def front_page():
    return render_template('front_page.html')


@app.route('/add_bookmark/', methods=['POST'])
def add_bookmark():
    short = request.form['short']
    link = request.form['link']
    return short + ' ' + link
