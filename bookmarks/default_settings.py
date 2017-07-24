import pkg_resources  # part of setuptools

USER_AGENT_NAME = 'bookmarks'
VERSION_NUMBER = pkg_resources.require('bookmarks')[0].version
SECRET_KEY = 'development key'
DATABASE_USERNAME = 'bookmarks'
DATABASE_PASSWORD = ''
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'bookmarks'
TEST_DATABASE_NAME = 'bookmarks_test'
