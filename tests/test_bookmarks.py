import os
import re
import unittest

import bookmarks


class BookmarksTestCase(unittest.TestCase):
    # Define a user
    user = {
        'username': 'byanofsky',
        'name': 'Brandon Yanofsky',
        'email': 'byanofsky@me.com',
        'password': 'Brandon123'
    }

    # Setup and teardown functions
    def setUp(self):
        self.app = bookmarks.app.test_client()
        bookmarks.database.init_db()

    def tearDown(self):
        bookmarks.database.db_session.remove()
        bookmarks.database.Base.metadata.drop_all(
            bind=bookmarks.database.engine)

    # Test helper functions
    def register(self, username, name, email, password, confirm=None):
        return self.app.post('/register_user/', data=dict(
            username=username,
            name=name,
            email=email,
            password=password,
            confirm=confirm
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login_user/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.post('/logout_user/', follow_redirects=True)

    def user_register(self):
        rv = self.register(
            self.user['username'],
            self.user['name'],
            self.user['email'],
            self.user['password'],
            confirm=self.user['password']
        )
        msg = 'Successfully registered {} {} {}'.format(
            self.user['username'],
            self.user['name'],
            self.user['email']
        )
        assert (msg.encode('utf-8') in rv.data)

    def user_login(self):
        rv = self.login(self.user['username'], self.user['password'])
        msg = 'Successfully logged in {}'.format(self.user['username'])
        assert (msg.encode('utf-8') in rv.data)

    def user_logout(self):
        rv = self.logout()
        assert (b'Successfully logged out' in rv.data)

    def add_bookmark(self, link, follow_redirects=False):
        return self.app.post('/add_bookmark/', data=dict(
            link=link,
            follow_redirects='y' if follow_redirects else None
        ), follow_redirects=True)

    # Begin test functions
    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'There aren\'t any bookmarks yet.' in rv.data

    def test_register_login_logout(self):
        # Register a new account
        self.user_register()
        # Logout
        self.user_logout()
        # Log back in
        self.user_login()
        # Log back out
        self.user_logout()

    def test_user_exist_register(self):
        # Create a new account
        self.user_register()
        # Logout
        self.user_logout()
        # Create a duplicate of that account
        rv = self.register(
            self.user['username'],
            self.user['name'],
            self.user['email'],
            self.user['password'],
            confirm=self.user['password']
        )
        # Check error message for existing username
        msg = 'A user already exists with the username {}'.format(
            self.user['username']
        )
        assert (msg.encode('utf-8') in rv.data)
        # Check error message for existing email
        msg = 'A user already exists with the email {}'.format(
            self.user['email']
        )
        assert (msg.encode('utf-8') in rv.data)

    def test_register_validation(self):
        username = 'bya'
        name = ''
        email = 'bya'
        password = 'Bra'
        confirm = ''
        # Check username length validation
        rv = self.register(username, name, email, password, confirm)
        msg = 'Username must be between 4 and 25 characters'
        assert (msg.encode('utf-8') in rv.data)
        # Check name validation
        msg = 'This field is required.'
        assert (msg.encode('utf-8') in rv.data)
        # Check email address length and email format
        msg = 'Invalid email address.'
        assert (msg.encode('utf-8') in rv.data)
        msg = 'Field must be between 6 and 35 characters long.'
        assert (msg.encode('utf-8') in rv.data)
        # Check password length and format
        msg = 'Password must be 5 to 18 characters long'
        assert (msg.encode('utf-8') in rv.data)
        msg = ('Password must include at least one lowercase letter, ' +
               'one uppercase letter, and one number.')
        assert (msg.encode('utf-8') in rv.data)

        # Make new request, check password confirmed
        rv = self.register(
            username='byanofsky',
            name='Brandon Yanofsky',
            email='byanofsky@me.com',
            password='Brandon123',
            confirm=''
        )
        msg = 'You must confirm your password'
        assert (msg.encode('utf-8') in rv.data)

    def test_login_user_pw_errors(self):
        # Register a new account
        self.user_register()
        self.user_logout()
        # Try username that does not exist
        rv = self.login('nouser', self.user['password'])
        assert (b'User does not exist' in rv.data)
        # Try incorrect password
        rv = self.login(self.user['username'], '12345')
        assert (b'Password incorrect' in rv.data)
        # Successful login
        self.user_login()

    def test_login_validation(self):
        # Register a new account
        self.user_register()
        rv = self.login(None, None)
        assert (b'Please enter a username' in rv.data)
        assert (b'Please enter a password' in rv.data)
        self.user_login()

    def test_add_bookmark(self):
        link = 'http://google.com/'
        # Register an account
        self.user_register()
        # Attempt to add bookmark
        rv = self.add_bookmark(link)
        assert (b'Successfully added' in rv.data)
        assert (link.encode('utf-8') in rv.data)
        m = re.search(b'(?<=Successfully added ).{6}', rv.data)
        b_id = m.group(0)
        # # Check that b_id redirects to link
        rv = self.app.get('/' + b_id.decode())
        assert rv.headers['Location'] == link
        # Visit a bookmark that does not exist
        rv = self.app.get('/fake12')
        assert rv.status_code == 404

    def test_add_many_bookmarks(self):
        bookmarks = [
            'http://www.google.com',
            'http://github.com',
            'http://amazon.com'
        ]
        # Register an account
        self.user_register()
        # Create bookmarks
        for b in bookmarks:
            self.add_bookmark(b)
        # Check that all bookmarks visible on homepage
        rv = self.app.get('/')
        for b in bookmarks:
            assert (b.encode('utf-8') in rv.data)

    def test_add_bookmark_redirects(self):
        # Google redirects to www
        link = 'http://google.com'
        r_link = 'http://www.google.com/'
        # Register an account
        self.user_register()
        # Add link and follow redirect
        rv = self.add_bookmark(link, follow_redirects=True)
        assert (b'Successfully added' in rv.data)
        assert (r_link.encode('utf-8') in rv.data)
        # Check that id leads to r_link
        m = re.search(b'(?<=Successfully added ).{6}', rv.data)
        b_id = m.group(0)
        rv = self.app.get('/' + b_id.decode())
        assert rv.headers['Location'] == r_link

    def test_add_bookmark_validation(self):
        # Register an account
        self.user_register()
        # Attempt to add bookmark
        rv = self.add_bookmark(link='www.google.com/')
        assert b'Link must be a properly formatted URL' in rv.data

    def test_add_bookmark_errors(self):
        # Register an account
        self.user_register()
        # Add a bookmark with a 400 error
        rv = self.add_bookmark('http://www.google.com/404')
        assert b'Please check your link. It leads to this error:' in rv.data
        # Add bookmark with a connection error
        rv = self.add_bookmark('http://fakewebsitegoogle.com')
        assert b'Could not connect to your link. Please check URL.' in rv.data
        # Simulate a timeout error
        rv = self.add_bookmark('http://github.com:81')
        assert b'There was a timeout error. Please check URL.' in rv.data


if __name__ == '__main__':
    # Make sure we are in testing mode and testing env
    app_env = os.environ.get('APPLICATION_ENVIRONMENT')
    if (bookmarks.app.config['TESTING'] is True and
            app_env == 'testing'):
            unittest.main()
    else:
        print('Need to be in a testing environment. ' +
              'Set APPLICATION_ENVIRONMENT to testing.')
