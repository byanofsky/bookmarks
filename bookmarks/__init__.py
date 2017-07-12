from flask import Flask
from flask.ext.bcrypt import Bcrypt
import flask_login

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('bookmarks.default_settings')
app.config.from_pyfile('settings.py', silent=True)
bcrypt = Bcrypt(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

import bookmarks.views
