import os
import shutil
import sys

import bupytest

sys.path.insert(0, './')

from cookiedb import CookieDB, exceptions

users = {
    'jaedson': {
        'name': 'Jaedson',
        'age': 15,
        'email': 'test@mail.com',
        'languages': [
            'python', 'javascript',
            'cpp', 'css', 'html',
            'typescript'
        ]
    },
    'pedro': {
        'name': 'Pedro',
        'age': 24,
        'email': 'test@mail.com',
        'languages': [
            'javascript', 'css', 'html',
            'typescript'
        ]
    },
    'maria': {
        'name': 'Maria',
        'age': 17,
        'email': 'test@mail.com',
        'languages': [
            'javascript', 'css', 'html',
            'golang'
        ]
    }
}


class TestDatabase(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.dbpath = os.path.join('tests', 'databases')

        if os.path.isdir(self.dbpath):
            shutil.rmtree(self.dbpath)

        os.mkdir(self.dbpath)
        self._my_database_path = os.path.join(self.dbpath, 'MyDatabase')

        self.cookiedb = CookieDB(
            database=self._my_database_path,
            key='my-secret-key'
        )

    def test_invalid_key_exception(self):
        try:
            CookieDB(database=self._my_database_path, key='other-key')
        except exceptions.InvalidDatabaseKeyError:
            self.assert_true(True, message='CookieDB not detected invalid key')

    def test_add(self):
        self.cookiedb.add('users/', users)

    def test_get(self):
        users_db = self.cookiedb.get('users/')
        self.assert_expected(users, users_db, message='"users/" not equal values')

    def test_update(self):
        self.cookiedb.update('users/jaedson/age', 16)
        users['jaedson']['age'] = 16

        user_age = self.cookiedb.get('users/jaedson/age')
        self.assert_expected(16, user_age, message='"users/jaedson/age" value not updated')

    def test_delete(self):
        self.cookiedb.delete('users/maria')
        users.pop('maria')
        
        maria_user = self.cookiedb.get('users/maria')
        self.assert_false(maria_user, message='"users/maria/" not deleted')

    def test_append(self):
        self.cookiedb.append('users/jaedson/languages', 'C#')
        users['jaedson']['languages'].append('C#')

        user_langs = self.cookiedb.get('users/jaedson/languages')
        self.assert_expected(user_langs, users['jaedson']['languages'],
                             message='append failed to "users/jaedson/languages"')


class TestDatabasePersistence(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self.cookiedb = CookieDB(
            database=os.path.join('tests', 'databases', 'MyDatabase'),
            key='my-secret-key'
        )

    def test_add_new_data(self):
        self.cookiedb.add('test/a', {'foo': 'bar'})
        self.cookiedb.add('test/b', {'bar': 'foo'})

    def test_get_previous_data(self):
        previous_data = self.cookiedb.get('users/')

        self.assert_expected(
            previous_data,
            users,
            message='Previous data don\'t match'
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
