# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

from functools import wraps
from typing import Any

from . import exceptions
from . import _document as document


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
        key: str,
        database_local: str = None
    ):
        """
        Initializes the `JSONHandler` class and prepares the
        encryption key.

        :param key: Any plain text;
        :param database_local: Database directory.
        """

        if not database_local:
            database_local = './'

        if not key or type(key) != str:
            raise exceptions.InvalidKeyError(f'Argument "key" must be of type "str", not "{type(key)}"')

        self._open_database = None
        self._document = document.Document(key, database_local)

    def checkout(self) -> str:
        """Return opened databsase name

        :return: Database name
        :rtype: str
        """

        return self._open_database

    def open(self, database: str) -> None:
        """
        Stores the name of the database if it exists,
        otherwise an exception `DatabaseNotFoundError`
        is thrown.

        :param database: Database name;
        :return: None.
        """

        database_exists = self._document.exists_document(database)

        if not database_exists:
            raise exceptions.DatabaseNotFoundError(f'Database {database} not found.')
        else:
            self._open_database = database

        try:
            self._document.get_document(database)
        except (exceptions.InvalidTokenError, exceptions.InvalidSignatureError):
            raise exceptions.InvalidDatabaseKeyError('Invalid database encryption key')

    def close(self) -> None:
        """Close a open database.

        An exception `NoOpenDatabaseError` will be thrown
        if no database is open.
        """

        if self._open_database:
            self._open_database = None
        else:
            raise exceptions.NoOpenDatabaseError('No open database.')

    def create_database(self, name: str, if_not_exists: bool = False) -> None:
        """
        Create a database at the location specified
        in **database local** in the `CookieDB`
        class instance.

        :param name: Database name;
        :param if_not_exists: If "True", exceptions will
        not be thrown if you are trying to create a
        database that already exists;
        :return: None.
        """

        if not self._document.exists_document(name):
            self._document.create_document(name)
        elif not if_not_exists:
            raise exceptions.DatabaseExistsError(f'Database {name} already exists.')

    def _get_database_items(self):
        try:
            database = self._document.get_document(self._open_database)
        except exceptions.DatabaseNotFoundError:
            self._open_database = None
            raise exceptions.DatabaseNotFoundError

        return database.get('items')

    def _get_path_list(self, path: str) -> str:
        path_list = path.split('/')
        if path.startswith('/'):
            path_list.pop(0)
        if path.endswith('/'):
            path_list.pop(-1)

        return path_list

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

        path_list = self._get_path_list(path)
        path_list_items = len(path_list) - 1

        for c, i in enumerate(path_list):
            if c == path_list_items:
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

        path_list = self._get_path_list(path)
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

        path_list = self._get_path_list(path)
        path_list_items = len(path_list) - 1

        for c, i in enumerate(path_list):
            if c == path_list_items:
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

            path_list = self._get_path_list(path)
            path_list_items = len(path_list) - 1

            for c, i in enumerate(path_list):
                if c == path_list_items:
                    items[i] = value
                else:
                    items = items.setdefault(i, {})

            self._document.update_document(self._open_database, database_items)
        else:
            raise exceptions.ItemNotExistsError(f'Item "{path}" not exists')

    def append(self, path: str, value: Any) -> None:
        """Append to a list from database. The path item
        must be a list, otherwise an exception will be thrown.

        :param path: Item path
        :type path: str
        :param value: Any value to append
        :type value: Any
        :raises exceptions.ItemIsNotAListError: If the path item is not a list
        :raises exceptions.ItemNotExistsError: If item not exists
        """

        data = self.get(path)

        if data is not None:
            if isinstance(data, list):
                data.append(value)
                self.add(path, data)
            else:
                raise exceptions.ItemIsNotAListError(f'Item "{path}" is not a list to append')
        else:
            raise exceptions.ItemNotExistsError(f'Item "{path}" not exists')
