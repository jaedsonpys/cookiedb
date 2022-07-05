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

from .json_handler import JSONHandler
from .exceptions import DatabaseNotFoundError, DatabaseExistsError, NoOpenDatabaseError

from typing import Union, Any
from functools import wraps


def required_database(method):
    @wraps(method)
    def wrapper(ref, *args, **kwargs):
        if ref.get_opened_database() is None:
            raise NoOpenDatabaseError('No open database.')
        else:
            return method(ref, *args, **kwargs)

    return wrapper


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

    def get_opened_database(self):
        return self._open_database

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

    @required_database
    def commit(self) -> bool:
        """
        Save changes made to the database.

        :return: Returns "True" if there were changes to commit.
        """

        if self._temp_items is None:
            return False

        self._json_handler.update_database(self._open_database, self._temp_items)
        return False

    @required_database
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
        path_list = path.split('/')
        path_list_filtered = []

        for i in path_list:
            if i != '':
                path_list_filtered.append(i)

        for c, i in enumerate(path_list_filtered):
            if c == (len(path_list_filtered) - 1):
                items = items.setdefault(i, value)
            else:
                items = items.setdefault(i, {})

        self._auto_commit()

    @required_database
    def get_item(self, path: Union[str, int]) -> Any:
        """
        Get a database item from the path.

        :param path: Item path;
        :return: Returns the obtained value.
        None if nothing is found.
        """

        path_list = path.split('/')
        last_items = {}

        database = self._json_handler.get_database(self._open_database)
        database_items = database.get('items')

        for i in path_list:
            if i != '':
                if not last_items:
                    db_item = database_items.get(i)
                    last_items = db_item
                else:
                    sub_item = last_items.get(i)
                    last_items = sub_item

        return last_items

    def delete(self, path: str) -> bool:
        database = self._json_handler.get_database(self._open_database)
        database_items = database.get('items')

        df = database_items

        path_list = path.split('/')
        path_list_filtered = []

        for i in path_list:
            if i != '':
                path_list_filtered.append(i)

        for c, i in enumerate(path_list_filtered):
            if c == (len(path_list_filtered) - 1):
                df = df.pop(i)
            else:
                df = df.setdefault(i, {})

        self._json_handler.update_database(self._open_database, database_items)
