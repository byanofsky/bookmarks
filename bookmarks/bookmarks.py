from flask import Flask, render_template, request

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('bookmarks.default_settings')
app.config.from_pyfile('settings.cfg', silent=True)


@app.route('/', methods=['GET'])
def front_page():
    return render_template('front_page.html')


@app.route('/add_bookmark/', methods=['POST'])
def add_bookmark():
    short = request.form['short']
    link = request.form['link']
    return short + ' ' + link
