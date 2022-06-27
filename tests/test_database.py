import os

from pyseqtest import SeqTest
from cookiedb import CookieDB


class TestDatabase(SeqTest):
    def __init__(self):
        super().__init__()
        self.cookiedb: CookieDB

    def setup(self):
        if not os.path.isdir('./databases'):
            os.mkdir('./databases')

        self.cookiedb = CookieDB(database_local='./databases')

    def test_create_database(self):
        self.cookiedb.create_database('MyDatabase', if_not_exists=True)
        self.cookiedb.create_database('PySGIDatabase', if_not_exists=True)

        self.is_true(os.path.isfile('./databases/MyDatabase'), msg_error='"MyDatabase" not created')
        self.is_true(os.path.isfile('./databases/PySGIDatabase'), msg_error='"PySGIDatabase" not created')


if __name__ == '__main__':
    TestDatabase().run()
