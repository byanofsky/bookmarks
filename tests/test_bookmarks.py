import bookmarks
import unittest


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

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'There aren\'t any bookmarks yet.' in rv.data

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
        username = 'byanofsky'
        name = 'Brandon Yanofsky'
        email = 'byanofsky@me.com'
        password = 'Brandon123'
        rv = self.register(username, name, email, password, confirm=password)
        msg = 'Successfully registered {} {} {}'.format(
            username,
            name,
            email
        )
        assert (msg.encode('utf-8') in rv.data)
        # Create a duplicate of that account
        rv = self.register(username, name, email, password, confirm=password)
        # Check error message for existing username
        msg = 'A user already exists with the username {}'.format(username)
        assert (msg.encode('utf-8') in rv.data)
        # Check error message for existing email
        msg = 'A user already exists with the email {}'.format(email)
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
            confirm='')
        msg = 'You must confirm your password'
        assert (msg.encode('utf-8') in rv.data)

    def test_login_user_pw_errors(self):
        # Register a new account
        username = 'byanofsky'
        name = 'Brandon Yanofsky'
        email = 'byanofsky@me.com'
        password = 'Brandon123'
        self.register(username, name, email, password, confirm=password)
        self.logout()
        # Try username that does not exist
        rv = self.login('nouser', password)
        assert (b'User does not exist' in rv.data)
        # Try incorrect password
        rv = self.login(username, '12345')
        assert (b'Password incorrect' in rv.data)
        # Successful login
        rv = self.login(username, password)
        msg = 'Successfully logged in {}'.format(username)
        assert (msg.encode('utf-8') in rv.data)

    def test_login_validation(self):
        # Register a new account
        username = 'byanofsky'
        name = 'Brandon Yanofsky'
        email = 'byanofsky@me.com'
        password = 'Brandon123'
        self.register(username, name, email, password, confirm=password)
        rv = self.login(None, None)
        assert (b'Please enter a username' in rv.data)
        assert (b'Please enter a password' in rv.data)

if __name__ == '__main__':
    unittest.main()
