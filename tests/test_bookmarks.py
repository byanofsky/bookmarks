import bookmarks
import unittest


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        bookmarks.app.config['DATABASE_NAME'] = bookmarks.app.config['TEST_DATABASE_NAME']
        bookmarks.app.testing = True
        self.app = bookmarks.app.test_client()
        with bookmarks.app.app_context():
            bookmarks.database.init_db()

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(bookmarks.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'There aren\'t any bookmarks yet.' in rv.data

if __name__ == '__main__':
    unittest.main()
