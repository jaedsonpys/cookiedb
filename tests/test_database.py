import os
import sys

import bupytest

sys.path.insert(0, './')

from cookiedb import CookieDB, exceptions


class TestDatabase(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        if not os.path.isdir('./tests/databases'):
            os.mkdir('./tests/databases')

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

        self.cookiedb = CookieDB(database_local='./tests/databases', autocommit=True)

    def test_create_database(self):
        self.cookiedb.create_database('MyDatabase', if_not_exists=True)
        self.cookiedb.create_database('PySGIDatabase', if_not_exists=True)

        self.assert_true(os.path.isfile('./tests/databases/MyDatabase.cookiedb'), message='"MyDatabase" not created')
        self.assert_true(os.path.isfile('./tests/databases/PySGIDatabase.cookiedb'), message='"PySGIDatabase" not created')

    def test_open_database(self):
        try:
            self.cookiedb.open('MyDatabase')
            self.cookiedb.open('PySGIDatabase')
        except exceptions.DatabaseNotFoundError as error:
            self.assert_true(False, message='DatabaseNotFoundError exception')

    def test_create_items_1(self):
        self.cookiedb.create_item('languages/programming', self.programming_languages)
        self.cookiedb.create_item('languages/markup', self.markup_languages)

    def test_get_items_1(self):
        languages_db = self.cookiedb.get_item('languages/programming')
        markup_languages = self.cookiedb.get_item('languages/markup')

        self.assert_true(languages_db == self.programming_languages, message='"languages/programming" not equal values')
        self.assert_true(markup_languages == self.markup_languages, message='"languages/markup" not equal values')

    def test_create_items_2(self):
        self.cookiedb.create_item('users/', self.users)

    def test_get_items_2(self):
        users_db = self.cookiedb.get_item('users/')
        self.assert_true(users_db == self.users, message='"users/" not equal values')

    def test_delete_item(self):
        self.cookiedb.delete('languages/programming/python')
        python_lang = self.cookiedb.get_item('languages/programming/python')
        self.assert_false(python_lang, message='"languages/programming/python" not deleted')


if __name__ == '__main__':
    bupytest.this()
