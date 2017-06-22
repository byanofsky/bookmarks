from flask import Flask
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('bookmarks.default_settings')
app.config.from_pyfile('settings.cfg', silent=True)
bcrypt = Bcrypt(app)

import bookmarks.views
