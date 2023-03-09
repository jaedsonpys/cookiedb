import os
import shutil
import sys

import bupytest

sys.path.insert(0, './')

from cookiedb import CookieDB, exceptions

programming_languages = {
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

MARKUP_LANGS = {
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

USERS = [
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


class TestDatabase(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.dbpath = './tests/databases'

        if os.path.isdir(self.dbpath):
            shutil.rmtree(self.dbpath)

        os.mkdir(self.dbpath)

        self.cookiedb = CookieDB(
            key='my-secret-key',
            database_local=self.dbpath
        )

    def test_create_database(self):
        self.cookiedb.create_database('MyDatabase', if_not_exists=True)
        self.assert_true(os.path.isfile(f'{self.dbpath}/MyDatabase.cookiedb'), message='"MyDatabase" not created')

    def test_no_open_database_error_1(self):
        try:
            self.cookiedb.close()
        except exceptions.NoOpenDatabaseError:
            self.assert_true(True, message='NoOpenDatabaseError exception')
        else:
            self.assert_true(False, message='"NoOpenDatabaseError" exception was not thrown')

    def test_open_database(self):
        try:
            self.cookiedb.open('MyDatabase')
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='DatabaseNotFoundError exception')

    def test_no_open_database_error_2(self):
        try:
            self.cookiedb.close()
        except exceptions.NoOpenDatabaseError:
            self.assert_true(False, message='Non open database')

        self.cookiedb.open('MyDatabase')

    def test_invalid_key_exception(self):
        db_2 = CookieDB(key='other-key', database_local=self.dbpath)
        db_2.create_database('TestKeyDatabase', if_not_exists=True)

        try:
            db_2.open('MyDatabase')
        except exceptions.InvalidDatabaseKeyError:
            self.assert_true(True, message='CookieDB not detected invalid key')

    def test_add_items_1(self):
        self.cookiedb.add('languages/programming', programming_languages)
        self.cookiedb.add('languages/markup', MARKUP_LANGS)

    def test_get_items_1(self):
        languages_db = self.cookiedb.get('languages/programming')
        markup_languages = self.cookiedb.get('languages/markup')

        self.assert_true(languages_db == programming_languages, message='"languages/programming" not equal values')
        self.assert_true(markup_languages == MARKUP_LANGS, message='"languages/markup" not equal values')

    def test_add_items_2(self):
        self.cookiedb.add('users/', USERS)

    def test_get_items_2(self):
        users_db = self.cookiedb.get('users/')
        self.assert_true(users_db == USERS, message='"users/" not equal values')

    def test_update_item(self):
        self.cookiedb.update('languages/programming/python/name', 'CPython')
        language_name = self.cookiedb.get('languages/programming/python/name')

        self.assert_expected('CPython', language_name, message='Language name not updated')

    def test_delete_item_1(self):
        self.cookiedb.delete('languages/programming/python')
        programming_languages.pop('python')
        
        python_lang = self.cookiedb.get('languages/programming/python')
        self.assert_false(python_lang, message='"languages/programming/python" not deleted')

    def test_append_item(self):
        user = {
            'name': 'Maria',
            'age': 17,
            'email': 'test@mail.com',
            'languages': [
                'javascript', 'css', 'html',
                'golang'
            ]
        }

        USERS.append(user)
        self.cookiedb.append('users/', user)
        users_db = self.cookiedb.get('users/')
        self.assert_expected(users_db, USERS, message='"append" failed')

    def test_delete_item_2(self):
        self.cookiedb.delete('languages/markup')
        markup_langs = self.cookiedb.get('languages/markup')
        self.assert_false(markup_langs, message='"languages/markup" not deleted')


class TestDatabasePersistence(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self.cookiedb = CookieDB(
            key='my-secret-key',
            database_local='./tests/databases'
        )

        self.cookiedb.open('MyDatabase')

    def test_add_new_data(self):
        self.cookiedb.add('test/a', {'foo': 'bar'})
        self.cookiedb.add('test/b', {'bar': 'foo'})

    def test_get_previous_data(self):
        previous_data = self.cookiedb.get('languages/programming')

        self.assert_expected(
            previous_data,
            programming_languages,
            message='Incorrect "languages/programming" data'
        )

    def test_get_new_data(self):
        test_a = self.cookiedb.get('test/a')
        test_b = self.cookiedb.get('test/b')

        self.assert_expected(
            test_a,
            {'foo': 'bar'},
            message='Incorrect "test/a" data'
        )

        self.assert_expected(
            test_b,
            {'bar': 'foo'},
            message='Incorrect "test/b" data'
        )


if __name__ == '__main__':
    bupytest.this()
