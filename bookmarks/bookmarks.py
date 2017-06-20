from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('bookmarks.default_settings')
app.config.from_pyfile('settings.cfg', silent=True)


@app.route('/', methods=['GET'])
def front_page():
    return 'Hello, World!'
