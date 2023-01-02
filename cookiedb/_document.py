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

import os
import ast
from datetime import datetime
from typing import Union

import secpickle
from cryptography import fernet
from secpickle import exceptions as sp_exceptions

from . import exceptions


class Document:
    def __init__(self, key: bytes, database_local: str) -> None:
        self._fernet = fernet.Fernet(key)
        self._document_local = database_local
        self._key = key.decode()

    @staticmethod
    def _save_file(file_content: str, filepath: str) -> None:
        with open(filepath, 'wb') as writer:
            writer.write(file_content)

    def exists_document(self, database: str) -> bool:
        document_path = os.path.join(self._document_local, database + '.cookiedb')
        return os.path.isfile(document_path)

    def _encrypt(self, obj: dict) -> str:
        encrypted_data = self._fernet.encrypt(str(obj).encode())
        pickle_file = secpickle.dumps(encrypted_data, self._key)
        return pickle_file

    def _decrypt(self, encrypted: bytes) -> dict:
        decrypted_data = self._fernet.decrypt(encrypted)
        data = ast.literal_eval(decrypted_data.decode())
        return data

    def create_document(self, name: str) -> dict:
        document_path = os.path.join(self._document_local, name + '.cookiedb')
        created_time = str(datetime.now().replace(microsecond=0))

        document = {
            'name': name,
            'created_at': created_time,
            'updated_at': created_time,
            'items': {}
        }

        data = self._encrypt(document)
        self._save_file(data, document_path)

        return document

    def get_document(self, database: str) -> Union[None, dict]:
        document_path = os.path.join(self._document_local, database + '.cookiedb')

        try:
            with open(document_path, 'rb') as reader:
                data = secpickle.load(reader, self._key)
        except FileNotFoundError:
            document = None
        except sp_exceptions.IntegrityUnconfirmedError:
            raise exceptions.InvalidDatabaseKeyError(f'Invalid key to "{database}" database')
        else:
            document = self._decrypt(data)

        return document

    def update_document(self, database: str, items: dict) -> None:
        document_path = os.path.join(self._document_local, database + '.cookiedb')

        document = self.get_document(database)
        update_time = datetime.now().replace(microsecond=0)

        document['items'] = items
        document['updated_at'] = str(update_time)

        encrypted_json = self._encrypt(document)
        self._save_file(encrypted_json, document_path)
