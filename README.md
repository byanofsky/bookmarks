# bookmarks

A bookmarking and link shortening software.

You can see a fully functioning example here: https://bay-bookmarks.herokuapp.com

## What It Does

Allows users to save URLs to shortened links.

An authentication system allows users to register accounts and save bookmarks to their accounts.

Each bookmark is a random, 6 character alphanumeric id, such as `a3fl4c`. When a user visits a route that matches that id (for example, `/a3fl4c`), they will be redirected to the URL that is saved to that unique ID.

A hit counter tracks how many times a shortened link is requested.

## Getting Started

These instructions will get the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project to a live system.

### Prerequisites

Included in this repo is a Vagrantfile which already has Python 3, virtualenv, and PostgreSQL installed. If you use your own, please see other prerequisites below.

You will need to have [Python 3](https://wiki.python.org/moin/BeginnersGuide/Download) installed, as well as pip, setuptools, and wheels. You most likely already have these 3 installed, but if not, you can find [instructions for installing them here](https://packaging.python.org/tutorials/installing-packages/#install-pip-setuptools-and-wheel).

I'd also recommend setting up a virtual environment using [virtualenv](https://packaging.python.org/tutorials/installing-packages/#optionally-create-a-virtual-environment).

Lastly, you will need a PostgreSQL database set up with a user that has access to the created database.

### Installing

1. Duplicate `default_settings.py` to a new directory called `instance` that should live at the same level as `setup.py`. Call this duplicated file `settings.py`.

2. Update `settings.py` with your own settings. You'll see settings that should be changed are marked with `TODO`.

3. Most importantly, you should change the `DATABASE_URI` for each environment's database. It should follow the basic structure of:
```
'postgresql://username:password@host/db_name'
```

4. For `SECRET_KEY`, the recommended way to generate a secret key is to run this in Python:
```
>>> import os
>>> os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
```

5. Install the bookmarks package. The `-e` installs it in editable mode.
```
pip install -e .
```

6. Set your environment variables:
```
export FLASK_APP=bookmarks
export FLASK_DEBUG=1
export APPLICATION_ENVIRONMENT='development'
```
The final environment variable needs to match with your environment: `'production'`, `'development'`, or `'testing'`. If none is set, `'development'` is used by default.

7. Create database schema by running in python:
```
>>> from bookmarks.database import init_db
>>> init_db()
```
If you are using multiple application environments, you will need to change your `APPLICATION_ENVIRONMENT` variable and run this for each.

8. Start the Flask development server with:
```
flask run
```
If you are running on a Vagrant machine, you will need to append ` -h 0.0.0.0` to run so it is publicly accessible. [More info here](http://flask.pocoo.org/docs/0.12/quickstart/#public-server).

## Running Tests

I've included a testing module which you can use to test all functionality. It uses the Python unittest library.

You must set '`APPLICATION_ENVIRONMENT`' to `'testing'` for the tests to run. This is to protect against making changes to dev and production databases.

To run the tests, from the root of the application, run:
```
python tests/test_bookmarks.py
```

Because the tests will make requests to external websites, you will need an internet connection. And it can sometimes take a little while to run since it is making requests to other websites.

## Deployment

Coming Soon!

## Built With

* [Flask](http://flask.pocoo.org/) - web framework
* [SQLalchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
* [psycopg2](http://initd.org/psycopg/) - PostgreSQL adapter for Python
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
