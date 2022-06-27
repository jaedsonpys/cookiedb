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
        database = self._json_handler.exists_database(database_name)

        if not database:
            raise DatabaseNotFoundError(f'Database {database_name} not found.')
        else:
            self._open_database = database_name

    def create_database(self, database_name, if_not_exists: bool = False):
        if not self._json_handler.exists_database(database_name):
            self._json_handler.create_json_database(database_name)
        else:
            if not if_not_exists:
                raise DatabaseExistsError(f'Database {database_name} already exists.')

    def commit(self) -> bool:
        if self._temp_items is None:
            return False

        self._json_handler.update_database(self._open_database, self._temp_items)
        return False

    def create_item(self, path: Union[str, int], value: Any) -> None:
        items = self._temp_items
        path_split = path.split('/')

        for c, i in enumerate(path_split):
            if c == (len(path_split) - 1):
                items = items.setdefault(i, value)
            else:
                items = items.setdefault(i, {})

        self._auto_commit()

    def get_item(self, path: Union[str, int]) -> Any:
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


if __name__ == '__main__':
    database = CookieDB(database_local='../databases-test')
    database.create_database('MyDatabase', if_not_exists=True)
    database.open('MyDatabase')

    database.create_item('languages/python', {
        'name': 'Python',
        'ext': '.py'
    })

    # commit database changes
    database.commit()

    # get items
    languages = database.get_item('languages')
    print(languages)

    python_lang = database.get_item('languages/python')
    print(python_lang)
