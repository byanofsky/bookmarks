import bookmarks
import unittest


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = bookmarks.app.test_client()
        with bookmarks.app.app_context():
            bookmarks.database.init_db()

    def tearDown(self):
        with bookmarks.app.app_context():
            bookmarks.database.db_session.remove()
            bookmarks.database.Base.metadata.drop_all(
                bind=bookmarks.database.engine)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'There aren\'t any bookmarks yet.' in rv.data

if __name__ == '__main__':
    unittest.main()
