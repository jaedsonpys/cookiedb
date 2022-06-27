import os

from pyseqtest import SeqTest
from cookiedb import CookieDB, exceptions


class TestDatabase(SeqTest):
    def __init__(self):
        super().__init__()
        self.cookiedb: CookieDB

    def setup(self):
        if not os.path.isdir('./databases'):
            os.mkdir('./databases')

        self.programming_languages = {
            'python': {
                'extension': '.py',
                'name': 'Python'
            },
            'javascript': {
                'extension': '.js',
                'name': 'JavaScript'
            },
            'cpp': {
                'extension': '.cpp',
                'name': 'C++'
            },
            'typescript': {
                'extension': '.ts',
                'name': 'TypeScript'
            },
            'csharp': {
                'extension': '.cs',
                'name': 'C#'
            }
        }

        self.markup_languages = {
            'html': {
                'extension': '.html',
                'name': 'HTML'
            },
            'xhtml': {
                'extension': '.xhtml',
                'name': 'XHTML'
            },
            'xml': {
                'extension': '.xml',
                'name': 'XML'
            }
        }

        self.users = [
            {
                'name': 'Jaedson',
                'age': 15,
                'email': 'test@mail.com',
                'languages': [
                    'python', 'javascript',
                    'cpp', 'css', 'html',
                    'typescript'
                ]
            },
            {
                'name': 'Pedro',
                'age': 24,
                'email': 'test@mail.com',
                'languages': [
                    'javascript', 'css', 'html',
                    'typescript'
                ]
            },
            {
                'name': 'Maria',
                'age': 17,
                'email': 'test@mail.com',
                'languages': [
                    'javascript', 'css', 'html',
                    'golang'
                ]
            }
        ]

        self.cookiedb = CookieDB(database_local='./databases', autocommit=True)

    def test_create_database(self):
        self.cookiedb.create_database('MyDatabase', if_not_exists=True)
        self.cookiedb.create_database('PySGIDatabase', if_not_exists=True)

        self.is_true(os.path.isfile('./databases/MyDatabase'), msg_error='"MyDatabase" not created')
        self.is_true(os.path.isfile('./databases/PySGIDatabase'), msg_error='"PySGIDatabase" not created')

    def test_open_database(self):
        try:
            self.cookiedb.open('MyDatabase')
            self.cookiedb.open('PySGIDatabase')
        except exceptions.DatabaseNotFoundError as error:
            self.is_true(False, msg_error='DatabaseNotFoundError exception')

    def test_create_items_1(self):
        self.cookiedb.create_item('languages/programming', self.programming_languages)
        self.cookiedb.create_item('languages/markup', self.markup_languages)

    def test_get_items_1(self):
        languages_db = self.cookiedb.get_item('languages/programming')
        markup_languages = self.cookiedb.get_item('languages/markup')

        self.is_true(languages_db == self.programming_languages, msg_error='"languages/programming" not equal values')
        self.is_true(markup_languages == self.markup_languages, msg_error='"languages/markup" not equal values')

    def test_create_items_2(self):
        self.cookiedb.create_item('users/', self.users)

    def test_get_items_2(self):
        users_db = self.cookiedb.get_item('users/')
        self.is_true(users_db == self.users, msg_error='"users/" not equal values')


if __name__ == '__main__':
    TestDatabase().run()
