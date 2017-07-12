from setuptools import setup

setup(
    name='bookmarks',
    packages=['bookmarks'],
    version='0.0.1',
    description='A bookmarking and link shortening service.',
    author='Brandon Yanofsky',
    author_email='byanofsky@me.com',
    include_package_data=True,
    install_requires=[
        'Flask',
        'SQLalchemy',
        'mysqlclient',
        'Flask-Bcrypt',
        'Flask-Login'
    ],
)
