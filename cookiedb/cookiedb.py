# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

from os import path
from typing import Any

from . import exceptions
from ._document import Document
from ._encrypt import Cryptography


class CookieDB:
    def __init__(self, database: str, key: str) -> None:
        """
        Initializes an instance for CookieDB database manipulation.

        :param database: Database path/name
        :param key: Any plain text key
        """

        if not key or type(key) != str:
            raise exceptions.InvalidKeyError(f'Argument "key" must be of type "str", not "{type(key)}"')
        
        if not database.endswith('.cookiedb'):
            database = database + '.cookiedb'

        _crypto = Cryptography(key)
        self._document = Document(_crypto, database)

        if not path.isfile(database):
            self._document.create_document()
        else:
            try:
                self._document.get_document()
            except (exceptions.InvalidTokenError, exceptions.InvalidSignatureError):
                raise exceptions.InvalidDatabaseKeyError('Invalid database encryption key')

    def _get_database_items(self):
        try:
            database = self._document.get_document()
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

        self._document.update_document(database_items)

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

        self._document.update_document(database_items)

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

            self._document.update_document(database_items)
        else:
            raise exceptions.ItemNotExistsError(f'Item "{path}" not exists')

    def append(self, path: str, value: Any) -> None:
        """Append to a list from database. The path item
        must be a list, otherwise an exception will be thrown.

        If the specified path does not exist, it will be created
        automatically containing a list.

        :param path: Item path
        :type path: str
        :param value: Any value to append
        :type value: Any
        :raises exceptions.ItemIsNotAListError: If the path item is not a list
        """

        data = self.get(path) or []

        if isinstance(data, list):
            data.append(value)
            self.add(path, data)
        else:
            raise exceptions.ItemIsNotAListError(f'Item "{path}" is not a list to append')
