import os
import pkg_resources  # part of setuptools

app_env = os.environ.get('APPLICATION_ENVIRONMENT') or 'development'

USER_AGENT_NAME = 'bookmarks'
VERSION_NUMBER = pkg_resources.require('bookmarks')[0].version
SECRET_KEY = 'development key'
TESTING = False
TIMEOUT = 5

if app_env == 'development':
    DATABASE_URI = ''
    DEBUG = True

if app_env == 'testing':
    TESTING = True
    TIMEOUT = 1
    WTF_CSRF_ENABLED = False
    DATABASE_URI = ''
