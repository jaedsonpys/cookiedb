from json_handler import JSONHandler
from exceptions import DatabaseNotFoundError


class CookieDB:
    def __init__(
        self,
        key: str = None,
        database_local: str = None
    ):
        self._json_handler = None
        self._open_database = None
        self._temp_database = None

        if not database_local:
            database_local = './'

        if not key:
            key = 't45tc90GyT4f4Qim0xt3BsSsZ5oEEgPbM9VstlGwfdg='

        self._key = key
        self._database_local = database_local

    def open(self, database_name: str) -> None:
        self._json_handler = JSONHandler(self._key, self._database_local)
        database = self._json_handler.exists_database(database_name)

        if not database:
            raise DatabaseNotFoundError(f'Database {database_name} not found.')
        else:
            self._open_database = database_name
