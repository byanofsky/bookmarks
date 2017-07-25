import bookmarks
import unittest


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = bookmarks.app.test_client()
        # with bookmarks.app.app_context():
        bookmarks.database.init_db()

    def tearDown(self):
        # with bookmarks.app.app_context():
        bookmarks.database.db_session.remove()
        bookmarks.database.Base.metadata.drop_all(
            bind=bookmarks.database.engine)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'There aren\'t any bookmarks yet.' in rv.data

    def register(self, username, name, email, password):
        return self.app.post('/register_user/', data=dict(
            username=username,
            name=name,
            email=email,
            password=password,
            confirm=password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password,
            confirm=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_register(self):
        username = 'byanofsky'
        name = 'Brandon Yanofsky'
        email = 'byanofsky@me.com'
        password = 'Brandon123'
        rv = self.register(username, name, email, password)
        # print(rv.data)
        assert (b'Successfully registered ' in rv.data)


if __name__ == '__main__':
    unittest.main()
