# bookmarks
A bookmarking and link shortening service.

## What It Does

Bookmarks allows users to save URLs to shortened links.

An authentication system allows users to register accounts and save bookmarks to their accounts.

Each bookmark is a random, 6 character alphanumeric id, such as `a3fl4c`. When a user visits a route that matches that id (for example, `/a3fl4c`), they will be redirected to the URL that is saved to that unique ID.

A hit counter tracks how many times a shortened link is requested.

## Getting Started

These instructions will get the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project to a live system.

### Prerequisites

You will need to have [Python 3](https://wiki.python.org/moin/BeginnersGuide/Download) installed, as well as pip, setuptools, and wheels. You most likely already have these 3 installed, but if not, you can find [instructions for installing them here](https://packaging.python.org/tutorials/installing-packages/#install-pip-setuptools-and-wheel).

I'd also recommend setting up a virtual environment using [virtualenv](https://packaging.python.org/tutorials/installing-packages/#optionally-create-a-virtual-environment).

Lastly, you will need a MySQL database set up with a user that has access to the created database.

### Installing

1. Duplicate `default_settings.py` to a new directory called `instance` that should live at the same level as `setup.py`. Call this duplicated file `settings.py`.

2. Update `settings.py` with your own settings, such as `DATABASE_USERNAME`, `DATABASE_PASSWORD`, etc.

3. For `SECRET_KEY`, the recommended way to generate a secret key is:
```
>>> import os
>>> os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
```

4. Install the bookmarks package. The `-e` install it in editable mode.
```
pip install -e .
```

5. Create database schema by running in python:
```
>>> from bookmarks.database import init_db
>>> init_db()
```

6. Start the Flask development server with:
```
export FLASK_APP=bookmarks
export FLASK_DEBUG=1
flask run
```
If you are running on a Vagrant machine, you will need to append ` -h 0.0.0.0` to run so it is publicly accessible. [More info here](http://flask.pocoo.org/docs/0.12/quickstart/#public-server).

## Running Tests

Coming Soon!

## Deployment

Coming Soon!

## Built With

* [Flask](http://flask.pocoo.org/) - web framework
* [SQLalchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
* [mysqlclient](https://pypi.python.org/pypi/mysqlclient) - interface to MySQL database server
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/) - Flask extension that provides bcrypt hashing utilities
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - Flask extension that provides user session management
* [WTForms](https://wtforms.readthedocs.io/en/latest/) - forms validation and rendering library for Python
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) - Flask extension that integrates WTForms
'requests'

## Authors

- [Brandon Yanofsky](https://github.com/byanofsky)

## License

Copyright 2017 Brandon Yanofsky

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
