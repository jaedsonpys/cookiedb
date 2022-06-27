# Copyright (C) 2022 by Jaedson Silva
# This code is licensed under MIT license (see LICENSE.txt for details)

from .json_handler import JSONHandler
from .exceptions import DatabaseNotFoundError, DatabaseExistsError

from typing import Union, Any


class CookieDB:
    def __init__(
        self,
        key: str = None,
        database_local: str = None,
        autocommit: bool = False
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

        self._json_handler = None
        self._open_database = None
        self._temp_items = {}

        if not database_local:
            database_local = './'

        if not key:
            key = 't45tc90GyT4f4Qim0xt3BsSsZ5oEEgPbM9VstlGwfdg='

        self._key = key
        self._database_local = database_local
        self._autocommit = autocommit

        self._json_handler = JSONHandler(self._key, self._database_local)

    def _auto_commit(self):
        if self._autocommit:
            self.commit()

    def open(self, database_name: str) -> None:
        """
        Stores the name of the database if it exists,
        otherwise an exception `DatabaseNotFoundError`
        is thrown.

        :param database_name: Database name;
        :return: None.
        """

        database_exists = self._json_handler.exists_database(database_name)

        if not database_exists:
            raise DatabaseNotFoundError(f'Database {database_name} not found.')
        else:
            self._open_database = database_name

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

        if not self._json_handler.exists_database(database_name):
            self._json_handler.create_json_database(database_name)
        else:
            if not if_not_exists:
                raise DatabaseExistsError(f'Database {database_name} already exists.')

    def commit(self) -> bool:
        """
        Save changes made to the database.

        :return: Returns "True" if there were changes to commit.
        """

        if self._temp_items is None:
            return False

        self._json_handler.update_database(self._open_database, self._temp_items)
        return False

    def create_item(self, path: Union[str, int], value: Any) -> None:
        """
        Creates an item in the database.
        Each path separated by "/" is a key in the JSON file.

        Values can be of type `str`, `int`,
        `float`, `dict`, `list`, or `tuple`.

        :param path: Item path;
        :param value: Item value;
        :return: None.
        """

        items = self._temp_items
        path_split = path.split('/')

        for c, i in enumerate(path_split):
            if c == (len(path_split) - 1):
                items = items.setdefault(i, value)
            else:
                items = items.setdefault(i, {})

        self._auto_commit()

    def get_item(self, path: Union[str, int]) -> Any:
        """
        Get a database item from the path.

        :param path: Item path;
        :return: Returns the obtained value.
        None if nothing is found.
        """

        path_split = path.split('/')
        item = {}

        database = self._json_handler.get_database(self._open_database)
        database_items = database.get('items')

        for i in path_split:
            if i != '':
                if not item:
                    db_item = database_items.get(i)
                    item = db_item
                else:
                    db_item = item.get(i)
                    item = db_item

        return item
