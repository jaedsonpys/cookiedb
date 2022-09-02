# CookieDB
# Copyright (C) 2022  Jaedson Silva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from ._document import JSONHandler
from . import exceptions

from typing import Any
from functools import wraps

import cryptography.fernet


def required_database(method):
    @wraps(method)
    def decorator(ref, *args, **kwargs):
        if ref.checkout() is None:
            raise exceptions.NoOpenDatabaseError('No open database.')
        else:
            return method(ref, *args, **kwargs)

    return decorator


class CookieDB:
    def __init__(
        self,
        key: str = None,
        database_local: str = None
    ):
        """
        Initializes the **JSONHandler** class and prepares the
        encryption key.

        All changes are saved in a temporary dictionary until
        a commit is made, so if `autocommit` is not enabled,
        use the `CookieDB.commit()` method.

        :param key: Encryption key;
        :param database_local: Database directory;
        :param autocommit: If "True", changes will be saved every
        time a database method is called.
        """

        self._document = None
        self._open_database = None

        if not database_local:
            database_local = './'

        if not key:
            key = 't45tc90GyT4f4Qim0xt3BsSsZ5oEEgPbM9VstlGwfdg='

        self._key = key
        self._database_local = database_local

        self._document = JSONHandler(self._key, self._database_local)

    def checkout(self):
        return self._open_database

    def open(self, database_name: str) -> None:
        """
        Stores the name of the database if it exists,
        otherwise an exception `DatabaseNotFoundError`
        is thrown.

        :param database_name: Database name;
        :return: None.
        """

        database_exists = self._document.exists_document(database_name)

        if not database_exists:
            raise exceptions.DatabaseNotFoundError(f'Database {database_name} not found.')
        else:
            self._open_database = database_name

        try:
            self._document.get_document(database_name)
        except cryptography.fernet.InvalidToken:
            raise exceptions.InvalidDatabaseKeyError('Invalid database key')

    def close(self) -> None:
        """Close a open database.

        An exception `NoOpenDatabaseError` will be thrown
        if no database is open.
        """

        if self._open_database:
            self._open_database = None
        else:
            raise exceptions.NoOpenDatabaseError('No open database.')

    def create_database(self, database_name, if_not_exists: bool = False) -> None:
        """
        Create a database at the location specified
        in **database local** in the `CookieDB`
        class instance.

        :param database_name: Database name;
        :param if_not_exists: If "True", exceptions will
        not be thrown if you are trying to create a
        database that already exists;
        :return: None.
        """

        if not self._document.exists_document(database_name):
            self._document.create_document(database_name)
        else:
            if not if_not_exists:
                raise exceptions.DatabaseExistsError(f'Database {database_name} already exists.')

    def _get_database_items(self):
        database = self._document.get_document(self._open_database)
        return database.get('items')

    def _filter_path_list(self, path_list: list) -> str:
        path_list_filtered = [i for i in path_list if i != '']
        return path_list_filtered

    @required_database
    def add(self, path: str, value: Any) -> None:
        """
        Creates an item in the database.
        Each path separated by "/" is a key in the JSON file.

        :param path: Item path;
        :param value: Item value;
        :return: None.
        """

        database_items = self._get_database_items()
        items = database_items

        path_list = self._filter_path_list(path.split('/'))

        for c, i in enumerate(path_list):
            if c == (len(path_list) - 1):
                items[i] = value
            else:
                items = items.setdefault(i, {})

        self._document.update_document(self._open_database, database_items)

    @required_database
    def get(self, path: str) -> Any:
        """
        Get a database item from the path.

        :param path: Item path;
        :return: Returns the obtained value.
        None if nothing is found.
        """

        path_list = self._filter_path_list(path.split('/'))
        last_items = {}

        database_items = self._get_database_items()

        for i in path_list:
            if not last_items:
                db_item = database_items.get(i)
                last_items = db_item
            else:
                sub_item = last_items.get(i)
                last_items = sub_item

        return last_items

    def delete(self, path: str) -> None:
        """Delete a item from database.

        If the item does not exist, nothing will
        be returned and no exception will be thrown.

        :param path: Item path
        :type path: str
        :return: None
        """

        database_items = self._get_database_items()
        df = database_items

        path_list = self._filter_path_list(path.split('/'))

        for c, i in enumerate(path_list):
            if c == (len(path_list) - 1):
                if i in df:
                    df = df.pop(i)
            else:
                df = df.setdefault(i, {})

        self._document.update_document(self._open_database, database_items)

    def update(self, path: str, value: Any) -> None:
        """Update a item from database.

        If the item does not exist, an
        exception will be thrown.

        :param path: Item path
        :type path: str
        :raises exceptions.ItemNotExistsError: 
        Raised if item does not exist
        """

        if self.get(path) is not None:
            database_items = self._get_database_items()
            items = database_items

            path_list = self._filter_path_list(path.split('/'))

            for c, i in enumerate(path_list):
                if c == (len(path_list) - 1):
                    items[i] = value
                else:
                    items = items.setdefault(i, {})

            self._document.update_document(self._open_database, database_items)
        else:
            raise exceptions.ItemNotExistsError(f'Item "{path}" not exists')
